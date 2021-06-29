from rest_framework import serializers

from app_ticket.models import Ticket, TicketMessage


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            'id',
            'owner',
            'category',
            'subject',
            'is_open',
            'last_update',
        )


class TicketMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = (
            'message',
            'file',
            'register_date',
            'is_reply',
        )
