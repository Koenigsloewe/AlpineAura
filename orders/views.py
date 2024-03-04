from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse, HttpResponse

from account.models import Address, Customer
from basket.basket import Cart
from .models import Order, OrderItem


# Create your views here.
@login_required
def add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        order_key = request.POST.get('order_key')
        user_id = request.user.id
        email = request.user.email
        phone = get_object_or_404(Customer, email=email).phone_number
        selected_address = get_object_or_404(Address, customer=user_id, default_address=True)
        cart_total = cart.get_total_price()

        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(user_id=user_id,
                                         full_name=selected_address.full_name,
                                         email=email,
                                         phone=phone,
                                         address1=selected_address.address_line,
                                         city=selected_address.town_city,
                                         post_code=selected_address.postcode,
                                         country_code=selected_address.country,
                                         total_paid=cart_total,
                                         payment_option='stripe',
                                         order_key=order_key,
                                         )
            order_id = order.pk
            for item in cart:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'],
                                         quantity=item['qty'])

        response = JsonResponse({'success': 'Return something'})
        return response


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders
