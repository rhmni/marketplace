from django.contrib import admin
from app_product.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'pk'
    )
