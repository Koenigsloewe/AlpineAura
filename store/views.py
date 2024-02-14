from django.shortcuts import render, get_object_or_404
from .models import Category, Product


# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


def product_page(request, category_slug, slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=slug, category=category)
    return render(request, 'store/product.html', {'product': product})
