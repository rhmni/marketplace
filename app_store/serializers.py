from rest_framework import serializers

from app_store.models import Store


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
