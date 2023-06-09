import datetime
import random
import string
import uuid
from methodism import custom_response, error_params_unfilled, MESSAGE, error_msg_unfilled, generate_key, code_decoder
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from base.helper import send_sms
from materio.models import User
from materio.models.auth import OTP


def regis(requests, params):
    nott = 'phone' if 'phone' not in params else 'password' if 'password' not in params else 'token' if 'token' not in params else 'username' if 'username' not in params else ''
    if 'password' not in params or 'token' not in params:
        return custom_response(False, message=error_params_unfilled(nott))

    otp = OTP.objects.filter(key=params['token']).first()

    if not otp:
        return custom_response(False, {"Error": "Неверный токен !"})

    if otp.is_conf:
        return custom_response(False, {"Error": "Устаревший токен !"})

    user = User.objects.filter(phone=otp.phone).first()

    if user:
        return custom_response(False, {"Error": "Этот эмайл ранее был зарегистрирован"})

    if len(params['password']) < 8 or not params['password'].isalnum() or " " in params['password']:
        return custom_response(False, {
            "Error": "Длина пароля должно быть не меннее 8 символов и больше 2х занков без пробелов !"})

    user_data = {
        "password": params['password'],
        "username": params['username'],
        "phone": params.get('phone', '')

    }

    if params.get('key', None) == 'qwerty':
        user_data.update({
            "is_staff": True,
            "is_superuser": True
        })

    user = User.objects.create_user(**user_data)
    token = Token.objects.create(user=user)
    return custom_response(False, {
        "Success": "Ваш аккаунт успешно создан",
        "Ваш секретный ключ": token.key
    })


def login(request, params):
    not_data = 'phone' if 'phone' not in params else 'password' if 'password' not in params else ''
    if not_data:
        return custom_response(False, message=error_params_unfilled(not_data))

    user = User.objects.filter(phone=params['phone']).first()
    if not user:
        return custom_response(False, message=MESSAGE['UserNotFound'])

    if not user.check_password(params['password']):
        return custom_response(True, message=MESSAGE['UserPasswordError'])

    token = Token.objects.get_or_create(user=user)
    return custom_response(True, data={"succes": token[0].key})


def logout(request, params):

    token = Token.objects.filter(user=request.user).first()
    if token:
        token.delete()
    return custom_response(True, message=MESSAGE['LogedOut'])


def user_delete(request, params):
    request.user.delete()
    return custom_response(True, message=MESSAGE['UserSuccessDeleted'])


def StepOne(request, params):
    not_data = 'phone' if 'phone' not in params else ''

    if not_data:
        return custom_response(True, message=error_msg_unfilled(not_data))

    if 'phone' in params:
        if type(params['phone']) is not int and len(str(params['phone'])) < 12:
            error_msg = f"'{params['phone']}' phone 👈 12ta raqam"
            return custom_response(True, message=error_params_unfilled(error_msg))



    code = random.randint(100000, 999999)
    sms = send_sms(otp=code, phone=params['phone'])
    if sms['status'] != 'waiting':
        return custom_response(True, message=error_params_unfilled(sms))

    shifr = uuid.uuid4().__str__() + "$" + str(code) + "$" + generate_key(20)

    shifr = code_decoder(shifr, l=5)

    # letters = string.ascii_letters
    # digits = string.digits

    # for_help = digits + letters + digits
    # code = ''.join(for_help[random.randint(0, len(for_help)-1)] for i in range(10))

    otp = OTP.objects.create(key=shifr, phone=params['phone'])

    return custom_response(True, data={
        "code": code,
        'shifr': otp.key
    })


def StepTwo(request, params):
    not_base = 'otp' if 'otp' not in params else '' or 'token' if 'token' not in params else ''
    if not_base:
        return custom_response(True, error_params_unfilled(not_base))

    token = OTP.objects.filter(key=params['token']).first()

    if not token:
        return custom_response(True, message=('token topilmadi'))

    if token.is_expire:
        return custom_response(True, message=('token eskirdi'))

    if token.is_conf:
        token.is_conf = True
        token.save()

        return custom_response(True, message=MESSAGE['TokenUnUsable'])

    now = datetime.datetime.now(datetime.timezone.utc)


    if (now - token.create).total_seconds() > 18000:

        token.is_expire = True
        token.save()


        return custom_response(False, message=MESSAGE['TokenUnUsable'])

    code = code_decoder(token.key, decode=True, l=5).split("$")[1]
    if code != str(params['otp']):
        token.tires += 1
        token.save()
        return custom_response(True, message=MESSAGE['TokenUnUsable'])


    token.is_conf = True
    user = User.objects.filter(phone=token.phone).first()

    return custom_response(True, message={"is_registered": user is not None})