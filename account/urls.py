from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .forms import UserLoginForm, ResetPasswordForm, ResetPasswordConfirmForm
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html', form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='user/reset-password.html',
                                                                 success_url='reset-password-email-confirm',
                                                                 email_template_name='user/reset-password-email.html',
                                                                 form_class=ResetPasswordForm),
         name='reset_password'),
    path('reset-password-confirm/<slug:uidb64>/<slug:token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='user/reset-password-confirm.html',
                                                     success_url='/account/reset-password-email-complete',
                                                     form_class=ResetPasswordConfirmForm), name='reset_password_confirm'),
    path('reset-password/reset-password-email-confirm', TemplateView.as_view(template_name='user/reset-status.html'), name='reset_password_done'),
    path('reset-password-email-complete', TemplateView.as_view(template_name='user/reset-status.html'), name='reset_password_complete')
]