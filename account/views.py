from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required

from orders.models import Order
from store.models import Product
from .forms import RegistrationForm, UserLoginForm, UserEditForm, UserAddressForm
from .models import Customer, Address
from .token import account_activation_token
from orders.views import user_orders


# Create your views here.
@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, 'user/dashboard.html', {'orders': orders})


def register(request):
    # if request.user.is_authenticated:
    #    redirect('/')

    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.email = register_form.cleaned_data['email']
            user.set_password(register_form.cleaned_data['password'])
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('registration/email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'user/reset-status.html')

    else:
        register_form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': register_form})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except():
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'registration/activation_invalid.html')


def custom_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('user_name')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('account:dashboard')
            else:
                # Return an 'invalid login' error message.
                return HttpResponse("Invalid login details")
        else:
            # Form is not valid
            return render(request, 'user/login.html', {'form': form})
    else:
        form = UserLoginForm()
        return render(request, 'user/login.html', {'form': form})


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'user/edit-details.html', {'user_form': user_form})


@login_required
def delete_user(request):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "user/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == 'POST':
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm()

    return render(request, "user/add-address.html", {"form": address_form})


@login_required
def edit_address(request, id):
    if request.method == 'POST':
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)

    return render(request, "user/edit-address.html", {"form": address_form})


@login_required
def delete_address(request, id):
    Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect("account:addresses")


@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user, default_address=True).update(default_address=False)
    Address.objects.filter(pk=id, customer=request.user).update(default_address=True)

    previous_url = request.META.get("HTTP_REFERER")

    if "delivery-address" in previous_url:
        return redirect("payment:delivery_address")

    return redirect("account:addresses")


@login_required
def wishlist(request):
    product = Product.objects.filter(user_wishlist=request.user)
    return render(request, "user/wishlist.html", {"wishlist": product})


@login_required
def add_item_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.user_wishlist.filter(id=request.user.id).exists():
        product.user_wishlist.remove(request.user)
        messages.success(request, f"Removed {product.product_title} of your wishlist")
    else:
        product.user_wishlist.add(request.user)
        messages.success(request, f"Added {product.product_title} to your wishlist")

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def delete_item_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.user_wishlist.filter(id=request.user.id).exists():
        product.user_wishlist.remove(request.user)
    else:
        product.user_wishlist.add(request.user)

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)

    return render(request, "user/user-orders.html", {"orders": orders})
