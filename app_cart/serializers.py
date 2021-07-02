from rest_framework import serializers


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(max_value=10, min_value=1)



