from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
import re

from .models import Customer, Address


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
        u = Customer.objects.filter(email=email)
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
        model = Customer
        fields = ('user_name', 'email')

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = Customer.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("username already exist")
        return user_name

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = Customer.objects.filter(email=email)
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


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email address (cannot be changed)',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400',
            'placeholder': 'Email',
            'id': 'form-email',
            'readonly': 'readonly'
        })
    )

    name = forms.CharField(
        label='Name',
        max_length=256,
        widget=forms.TextInput(attrs={
            'class': 'block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400',
            'placeholder': 'Name',
            'id': 'form-name'
        })
    )

    about = forms.CharField(
        label='About',
        widget=forms.Textarea(attrs={
            'class': 'block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400',
            'placeholder': 'About you',
            'id': 'form-about',
            'rows': 3
        }),
        required=False
    )

    phone_number = forms.CharField(
        label='Phone Number',
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400',
            'placeholder': 'Phone Number',
            'id': 'form-phone-number'
        }),
        required=False
    )

    class Meta:
        model = Customer
        fields = ('email', 'name', 'about', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True

    def clean_name(self):
        name = self.cleaned_data['name']
        # Example: Add validation logic here, e.g., checking length or format
        if len(name) < 2:
            raise ValidationError("Name must be at least 2 characters long.")
        return name

    def clean_about(self):
        about = self.cleaned_data['about']
        # Example: Validate the length of the about text
        if len(about) > 500:  # Assuming a max length of 500 characters
            raise ValidationError("The about section must not exceed 500 characters.")
        return about

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        # Example: Validate phone number format (simple regex example)
        if phone_number and not re.match(r'^\+?1?\d{9,15}$', phone_number):
            raise ValidationError("Please enter a valid phone number.")
        return phone_number


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "address_line", "postcode", "town_city", "country"]

    def __init__(self, *args, **kwargs):
        super(UserAddressForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({
            'class': 'block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400',
            'placeholder': 'Full Name'})
        self.fields['address_line'].widget.attrs.update({
            'class': 'block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400',
            'placeholder': 'Address Line'})
        self.fields['postcode'].widget.attrs.update({
            'class': 'block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400',
            'placeholder': 'Postcode'})
        self.fields['town_city'].widget.attrs.update({
            'class': 'block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400',
            'placeholder': 'Town/City'})
        self.fields['country'].widget.attrs.update({
            'class': 'block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400',
            'placeholder': 'Country'})
