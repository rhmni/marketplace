import re
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

from app_ticket.managers import OpenTicketsManager
from app_ticket.tasks import send_sms


class Ticket(models.Model):
    CATEGORIES = (
        ('T', 'technical'),
        ('F', 'financial'),
        ('O', 'orders'),
        ('E', 'etc'),
    )

    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets',
    )
    category = models.CharField(max_length=50, choices=CATEGORIES)
    subject = models.CharField(max_length=200)
    is_open = models.BooleanField(default=True)
    last_update = models.DateTimeField(null=True, blank=True)
    open_date = models.DateTimeField()
    close_date = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()
    opentickets = OpenTicketsManager()

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):

        if not self.pk:
            self.last_update = datetime.now()

        super().save(*args, **kwargs)


class TicketMessage(models.Model):
    ticket = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE,
        related_name='ticketmessages',
    )
    message = models.TextField()
    file = models.FileField(null=True, blank=True)
    register_date = models.DateTimeField()
    is_reply = models.BooleanField(default=False)

    def __str__(self):
        return self.message[:20]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_reply:
            send_sms.delay(self.ticket.owner.phone, f'you have new message for {self.ticket.subject} ticket')

        self.ticket.last_update = datetime.now()
        self.ticket.save()

    def clean(self):
        if not self.ticket.is_open:
            raise ValidationError('this ticket is already closed')
