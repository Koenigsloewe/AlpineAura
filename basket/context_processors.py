# context processors
from .basket import Cart


def get_cart(request):
    return {'Cart': Cart(request)}
