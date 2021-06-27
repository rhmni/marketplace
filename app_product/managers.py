from django.db import models


class ConfirmedProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_confirm=True)
