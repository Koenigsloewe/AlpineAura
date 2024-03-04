from  django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('shop/<slug:category_slug>/<slug:slug>', views.product_page, name='product'),
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),
    path('about-us/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('size-guides/', views.size_guides, name='size guides'),
    path('return-policy/', views.return_policy, name='return policy'),
    path('privacy-policy/', views.privacy_policy, name='privacy policy'),
    path('terms-of-service/', views.terms_of_service, name='terms of service'),
    ]
