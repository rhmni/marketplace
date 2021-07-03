from celery import shared_task
from django.conf import settings
from kavenegar import *
from datetime import timedelta, datetime

from app_ticket import models


@shared_task
def send_sms(phone, message):
    api = KavenegarAPI(
        settings.KAVENEGAR_SECRET_KEY
    )
    params = {
        'sender': '',
        'receptor': phone,
        'message': message,
    }
    response = api.sms_send(params)


@shared_task
def close_open_tickets():
    """
        Close tickets that are open before 24 hours
        And send sms to the user to know that his ticket is closed.
    """

    tickets = models.Ticket.opentickets.filter(
        last_update__lte=datetime.now() - timedelta(hours=24),
    )

    api = KavenegarAPI(
        settings.KAVENEGAR_SECRET_KEY
    )

    for ticket in tickets:
        params = {
            'sender': '',
            'receptor': ticket.owner.phone,
            'message': f'your ticket with subject {ticket.subject} has closed.',
        }
        response = api.sms_send(params)

    tickets.update(
        is_open=False,
        close_date=datetime.now(),
    )
