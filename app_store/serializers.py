from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app_store.models import Store, StoreCheckout


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = (
            'founder',
            'name',
            'slug',
            'description',
            'register_date',
            'wallet',
            'bank_number',
        )

        read_only_fields = (
            'founder',
            'register_date',
            'wallet',
        )


class CretaeStoreCheckoutSerializer(serializers.Serializer):
    bank_number = serializers.IntegerField(required=False)
    amount = serializers.IntegerField()

    def validate_bank_number(self, value):
        if len(str(value)) != settings.BANK_NUMBER_LENGTH:
            raise ValidationError(f'bank number must be {settings.BANK_NUMBER_LENGTH} digit')
        return value

    def validate_amount(self, value):
        if not settings.MIN_CHECKOUT <= value <= settings.MAX_CHECKOUT:
            raise ValidationError(f'your amount must between {settings.MIN_CHECKOUT} and {settings.MAX_CHECKOUT} toman')
        return value


class StoreCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreCheckout
        fields = (
            'pay_date',
            'bank_number',
            'amount',
        )
