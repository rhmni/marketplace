from rest_framework import serializers

from app_product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'image',
            'category',
            'description',
            'price',
            'stock',
        )
