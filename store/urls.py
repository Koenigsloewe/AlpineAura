from  django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/<slug:category_slug>/<slug:slug>', views.product_page, name='product'),
    #path('shop/<slug:category_slug>/', views.category_list, name='category_list'),
]
