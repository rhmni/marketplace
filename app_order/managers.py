from datetime import datetime

from django.db import models


class ActiveCouponManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True,
                                             valid_from__lt=datetime.now(),
                                             valid_to__gt=datetime.now(),
                                             )
