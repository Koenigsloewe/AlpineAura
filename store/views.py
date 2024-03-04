from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404

from AlpineAura.settings import RECIPIENT_LIST
from .models import Category, Product, ProductSpecificationValue


# Create your views here.

def home(request):
    products = Product.objects.all()
    latest_products = Product.objects.order_by('-created_at')[:8]
    latest_product_ids = latest_products.values_list('id', flat=True)

    random_products = Product.objects.exclude(id__in=list(latest_product_ids)).order_by('?')[:4]

    return render(request, 'store/home.html',
                  {'products': products, 'latest_products': latest_products, 'random_products': random_products})


def product_page(request, category_slug, slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=slug, category=category)
    product_specifications = ProductSpecificationValue.objects.filter(product=product)

    related_products = Product.objects.filter(category=category).exclude(id=product.id).order_by('-created_at')[:4]

    return render(request, 'store/product.html', {'product': product,
                                                  'product_specifications': product_specifications,
                                                  'related_products': related_products
                                                  })


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(
        category__in=category.get_descendants(include_self=True)
    )
    return render(request, "store/category.html", {"category": category, "products": products})


def about(request):
    return render(request, 'store/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        send_mail(
            subject=f"{subject} from {name}",
            message=message,
            from_email=email,
            recipient_list=RECIPIENT_LIST
        )

        messages.success(request, "Your message has been sent successfully!")

        return render(request, 'store/contact.html')
    else:
        return render(request, 'store/contact.html')


def return_policy(request):
    return render(request, 'store/return-policy.html')


def size_guides(request):
    return render(request, 'store/size-guides.html')


def privacy_policy(request):
    return render(request, 'store/privacy-policy.html')


def terms_of_service(request):
    return render(request, 'store/terms-of-service.html')


def shop(request):
    categories = Category.objects.all()
    return render(request, 'store/shop.html', {'categories': categories})
