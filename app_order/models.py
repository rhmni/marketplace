from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from app_order.managers import ActiveCouponManager
from app_product.models import Product


class Order(models.Model):
    STATUS = (
        ('R', 'received'),
        ('P', 'posted'),
        ('N', 'not posted'),
    )

    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
    )
    total_price = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(null=True, blank=True)
    pay_price = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, choices=STATUS, default='N')
    pay_date = models.DateTimeField()

    def __str__(self):
        return str(self.pay_price)


class OrderItem(models.Model):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='orderitems',
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='orderitems',
    )
    price = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.product.name

    def total_price(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        self.total_price()
        return super().save(*args, **kwargs)


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], help_text='percent')
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveCouponManager()

    def __str__(self):
        return self.code
