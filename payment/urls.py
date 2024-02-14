from django.urls import path

from payment import views

app_name = 'payment'

urlpatterns = [
    path('', views.checkout, name='checkout'),
    #path('orderplaced/', views.order_placed, name='order_placed'),
    #path('webhook/', views.stripe_webhook)
]
