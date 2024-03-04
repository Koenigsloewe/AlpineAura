from django.contrib import admin

# Register your models here.
from .models import DeliveryOptions, PaymentSelection

admin.site.register(DeliveryOptions)
admin.site.register(PaymentSelection)
