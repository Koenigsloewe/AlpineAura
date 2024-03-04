from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings

from payment.models import DeliveryOptions
from store.models import Product


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if settings.CART_SESSION_ID not in request.session:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, product_qty):
        product_id = str(product.id)

        price = product.discount_price if product.discount_price else product.regular_price

        if product_id not in self.cart:
            self.cart[product_id] = {'price': str(price), 'qty': int(product_qty)}

        self.save()

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        products_id = self.cart.keys()
        products = Product.objects.filter(id__in=products_id)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = (item['price'] * item['qty']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            yield item

    def get_subtotal_price(self):
        total_price = sum(Decimal(item['price']) * Decimal(item['qty']) for item in self.cart.values())
        return total_price

    def get_delivery_price(self):
        newprice = 0.00

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        return newprice

    def get_total_price(self):
        newprice = 0.00
        subtotal = self.get_subtotal_price()

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        total = subtotal + Decimal(newprice)
        return total

    def get_total_item_price(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            item = self.cart[product_id]
            total_price = Decimal(item['price']) * item['qty']
            return total_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return Decimal('0.00')

    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.save()

    def update(self, product_id, product_qty):
        product = str(product_id)

        if product in self.cart:
            self.cart[product]['qty'] = product_qty

        self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        del self.session["address"]
        del self.session["purchase"]
        self.save()

    def cart_update_delivery(self, delivery_price=0):
        subtotal = self.get_subtotal_price()
        total = subtotal + Decimal(delivery_price)
        return total
