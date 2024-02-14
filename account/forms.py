from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm

from .models import UserBase


class ResetPasswordConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={
        'class': 'block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400',
        'placeholder': '*******'}))
    new_password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={
        'class': 'block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400',
        'placeholder': '*******'}))


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400',
        'placeholder': 'Email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u.exists():
            raise forms.ValidationError(
                'If an account exists with the email provided, we will send an email with instructions to reset your password.')
        return email


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required',
                             error_messages={'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email')

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("username already exist")
        return user_name

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = UserBase.objects.filter(email=email)
        if r.count():
            raise forms.ValidationError("email already exist")
        return email

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['password'] != cleaned_data['password2']:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data['password2']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update({
            'class': 'block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400',
            'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({
            'class': 'block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400',
            'placeholder': 'youremail@domain.com'})
        self.fields['password'].widget.attrs.update({
            'class': 'block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400'})
        self.fields['password2'].widget.attrs.update({
            'class': 'block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400'})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email', widget=forms.TextInput(attrs={
        'class': 'block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400',
        'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400',
        'placeholder': '*******'}))
