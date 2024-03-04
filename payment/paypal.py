import sys
import os

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from django.conf import settings


class PayPalClient:
    def __init__(self):
        self.client_id = os.environ.get('PAYPAL_CLIENT_ID')
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)
