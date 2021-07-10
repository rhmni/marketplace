from django.db import models


class ConfirmedCommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_confirm=True)
