from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, UserLoginForm
from .models import UserBase
from .token import account_activation_token


# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'user/dashboard.html', {})


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
            return HttpResponse('registered successfully and activation send by email')

    else:
        register_form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': register_form})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
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
            print(username, password)
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
