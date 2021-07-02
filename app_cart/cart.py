from app_order.models import Coupon
from app_product.models import Product
from django.conf import settings


# Fake Data
# session = {
#     'cart': {
#         '1': {
#             'quantity': 2,
#             'total_price': 2000,
#         },
#         '6': {
#             'quantity': 2,
#             'total_price': 8000,
#         },
#         'pay_price': 7500.0,
#         'discount': 2500.0,
#         'final_price': 10000,
#     }
# }


class Cart:

    def __init__(self, request):
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

        self.cart['discount'] = 0
        self.cart['final_price'] = 0
        self.cart['pay_price'] = 0

    def add(self, product_id: int, quantity: int = 1):
        product_id = str(product_id)
        self.cart[product_id] = {'quantity': quantity, }

    def remove(self, product_id: int):
        product_id = str(product_id)
        try:
            del self.cart[product_id]
        except KeyError:
            pass

    def clear(self):
        del self.session[settings.CART_SESSION_ID]

    def get_list(self, coupon=None):
        self._check_product_exists()
        self._set_total_price()
        self._set_coupon(coupon)
        return self.cart

    def _set_coupon(self, coupon):
        cart = self.cart
        try:
            coupon = Coupon.active.get(code=coupon)
            cart['discount'] = (coupon.discount / 100) * cart['final_price']
            cart['pay_price'] = cart['final_price'] - cart['discount']
            if cart['pay_price'] < 0:
                cart['pay_price'] = 0
        except Coupon.DoesNotExist:
            cart['pay_price'] = cart['final_price']

    def _set_total_price(self):
        cart = self.cart
        product_ids = [product_id for product_id in self.cart.keys() if product_id.isnumeric()]
        products = Product.confirmed.filter(id__in=product_ids)
        for product in products:
            cart[str(product.id)]['total_price'] = product.price * cart[str(product.id)]['quantity']
            cart['final_price'] += cart[str(product.id)]['total_price']

    def _check_product_exists(self):
        cart = self.cart
        product_ids = [product_id for product_id in self.cart.keys() if product_id.isnumeric()]
        for product_id in product_ids:
            try:
                Product.confirmed.get(pk=product_id)
            except Product.DoesNotExist:
                del cart[product_id]
