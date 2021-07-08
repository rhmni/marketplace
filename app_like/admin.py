from django.contrib import admin

from app_like.models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
