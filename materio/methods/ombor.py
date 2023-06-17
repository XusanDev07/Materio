from methodism import custom_response, MESSAGE, error_params_unfilled

from materio.models import Basket, Maxsulot


def basket_add(request, params):
    if 'product_id' not in params:
        return custom_response(True, message={MESSAGE['ParamsNotFull']})

    root = Maxsulot.objects.filter(id=params['product_id']).first()
    if not root:
        return custom_response(False, message=error_params_unfilled(root))

    savat = Basket.objects.get_or_create(product=root, user=request.user)[0]
    savat.quent = params.get('quent', savat.quent)
    savat.save()

    return custom_response(True, message={"Succes": "Savatga qo'shildi"})


def get_savat(request, params):
    return custom_response(
        True,
        message={
            "result": [x.format() for x in Basket.objects.filter(user=request.user, status=True)]
        }
    )
