from django.contrib import admin

from app_comment.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
