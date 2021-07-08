from django.conf import settings
from django.db import models

from app_product.models import Product


class Like(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    register_date = models.DateTimeField()

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return str(self.register_date)
