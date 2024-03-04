from django.urls import path

from payment import views

app_name = 'payment'

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('orderplaced/', views.order_placed, name='order_placed'),
    path('error/', views.Error.as_view(), name='error'),
    path('webhook/', views.stripe_webhook),
    path("delivery-choices", views.delivery_choices, name="delivery_choices"),
    path("cart-update_delivery/", views.cart_update_delivery, name="cart_update_delivery"),
    path("delivery-address/", views.delivery_address, name="delivery_address"),
    path("payment-selection/", views.payment_selection, name="payment_selection"),
    path("payment-complete/", views.payment_complete, name="payment_complete"),
]
