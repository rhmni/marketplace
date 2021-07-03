from django.contrib import admin

from app_order.models import Coupon, OrderItem, Order


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass