from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app_bookmark.models import Bookmark
from app_product.models import Product


class CreateBookmarkSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        try:
            Product.confirmed.get(pk=product_id)
        except Product.DoesNotExist:
            raise ValidationError('product with this id does not exist')

        return product_id


class BookmarkProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'image',
            'price',
        )


class ListBookmarkSerializer(serializers.ModelSerializer):
    product = BookmarkProductDetailSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = (
            'product',
        )
