from django.db import models


class OpenTicketsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_open=True)
