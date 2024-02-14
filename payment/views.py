import json

import stripe
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from basket.basket import Cart
#from orders.views import payment_confirmation

@login_required
def checkout(request):
    cart = Cart(request)
    total = (str(cart.get_total_price())).replace('.', '')  # converting so an int because stripe is dumb
    total = int(total)

    stripe.api_key = 'sk_test_51OjR38HrB7JipLatLYv6fQK2Wd6TKpSdbeXyLZOzCm2lALP59jboreXHSRrJOBN0nVpmOohq9hCO4O79YNWDDV7O00X1qOhj6Q'
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='eur',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/checkout.html', {'client_secret': intent.client_secret})
"""
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)
    else:
        print('Unhandled event type UWU {}'.format(event.type))

    return HttpResponse(status=200)


def order_placed(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'payment/orderplaced.html')
"""