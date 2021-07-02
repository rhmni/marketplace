from django.contrib import admin

from app_order.models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    pass
