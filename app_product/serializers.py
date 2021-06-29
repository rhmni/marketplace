from rest_framework import serializers

from app_product.models import Product


class ProductGetSerializer(serializers.ModelSerializer):
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


class ProfileProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'seller',
            'category',
            'name',
            'image',
            'description',
            'price',
            'stock',
        )

        read_only_fileds = (
            'seller',
        )
