from datetime import datetime

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from app_cart.cart import Cart
from app_order.models import OrderItem, Order
from app_product.models import Product
from app_ticket.tasks import send_sms


class OrderCheckoutView(GenericAPIView):
    """
        checkout for order
    """

    permission_classes = (
        IsAuthenticated,
    )

    def get(self, request, coupon=None):

        cart = Cart(request)
        cart_detail = cart.detail(coupon)
        product_ids = [product_id for product_id in cart_detail.keys() if product_id.isnumeric()]
        if len(product_ids) == 0:
            return Response({'message': 'your cart is empy'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(owner=request.user, pay_date=datetime.now())

        for product_id in product_ids:
            product = Product.confirmed.get(pk=product_id)
            product.stock -= cart_detail[product_id]['quantity']
            product.sales_number += cart_detail[product_id]['quantity']
            product.seller.wallet += cart_detail[product_id]['total_price']
            product.seller.save()
            product.save()

            OrderItem.objects.create(
                order=order,
                product=product,
                price=product.price,
                quantity=cart_detail[product_id]['quantity'],
            )

        order.total_price = cart_detail['final_price']
        order.pay_price = cart_detail['pay_price']
        order.discount = cart_detail['discount']
        order.save()
        cart.clear()
        send_sms.delay(request.user.phone, 'your cart is paid success.')
        return Response({'message': 'your cart is paid success.'}, status=status.HTTP_200_OK)
