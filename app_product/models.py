from datetime import datetime

from django.db import models

from app_product.managers import ConfirmedProductManager
from app_store.models import Store


class Category(models.Model):
    sub_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcategories',
        null=True,
        blank=True,
        limit_choices_to={
            'is_sub': False,
        },
    )
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    register_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Product(models.Model):
    seller = models.ForeignKey(
        to=Store,
        on_delete=models.CASCADE,
        related_name='products',
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='products',
    )
    name = models.CharField(max_length=150)
    image = models.ImageField()
    description = models.TextField()
    price = models.PositiveBigIntegerField(default=0)
    sales_number = models.PositiveSmallIntegerField(default=0)
    stock = models.PositiveSmallIntegerField(default=0)
    is_confirm = models.BooleanField(default=False)
    is_exists = models.BooleanField(default=False)
    register_date = models.DateTimeField()

    objects = models.Manager()
    confirmed = ConfirmedProductManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if self.stock == 0:
            self.is_exists = False
        else:
            self.is_exists = True

        if not self.pk:
            self.register_date = datetime.now()

        super(Product, self).save(*args, **kwargs)
