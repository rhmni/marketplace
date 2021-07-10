from datetime import datetime

from django.conf import settings
from django.db import models

from app_comment.managers import ConfirmedCommentManager
from app_product.models import Product


class Comment(models.Model):
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    product = models.ForeignKey(
        Product,
        limit_choices_to={
            'is_confirm': True,
        },
        on_delete=models.CASCADE,
        related_name='comments',
    )

    sub_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcomments',
        null=True,
        blank=True,
    )

    is_sub = models.BooleanField(default=False)
    body = models.TextField()
    register_date = models.DateTimeField()
    is_confirm = models.BooleanField(default=False)

    objects = models.Manager()
    confirmed = ConfirmedCommentManager()

    def __str__(self):
        return self.body[:20]

    def save(self, *args, **kwargs):

        if self.sub_comment:
            self.is_sub = True

        if not self.register_date:
            self.register_date = datetime.now()

        super(Comment, self).save(*args, **kwargs)
