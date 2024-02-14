from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .basket import Cart

from store.models import Product


# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    return render(request, 'store/cart.html', {'Cart': cart})


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, product_qty=product_qty)
        cart_qty = cart.__len__()
        response = JsonResponse({'qty': cart_qty})
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        cart.delete(product=product_id)
        cart_qty = cart.__len__()
        cart_total_price = cart.get_total_price()
        response = JsonResponse({'qty': cart_qty, 'subtotal': cart_total_price})
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        cart.update(product_id=product_id, product_qty=product_qty)
        cart_qty = cart.__len__()
        cart_total_price = cart.get_total_price()
        total_item_price = cart.get_total_item_price(product_id)
        response = JsonResponse({'qty': cart_qty, 'subtotal': cart_total_price, 'totalItemPrice': total_item_price})
        return response
