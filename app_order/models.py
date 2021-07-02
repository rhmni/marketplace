from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from app_order.managers import ActiveCouponManager


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
