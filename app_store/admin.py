from django.contrib import admin
from app_store.models import Store, StoreCheckout


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'founder',
        'wallet',
        'register_date',

    )
    list_filter = (
        'register_date',
    )


@admin.register(StoreCheckout)
class StoreCheckoutAdmin(admin.ModelAdmin):
    list_display = (
        'store',
        'id',
        'amount',
        'pay_date',
        'bank_number',
    )
    list_filter = (
        'pay_date',
    )
    ordering = ('-id',)
    date_hierarchy = 'pay_date'
