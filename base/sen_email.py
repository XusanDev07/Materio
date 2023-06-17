from django.core.mail import send_mail


def send_email(OTP, email):
    subject = 'Xusandan salom'
    message = f'One Time Password {OTP}'
    from_email = 'xusanxalilov707@gmail.com'
    recipient_list = [f'{email}']

    send_mail(subject, message, from_email, recipient_list)