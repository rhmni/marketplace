from rest_framework import serializers

from app_ticket.models import Ticket, TicketMessage


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            'id',
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


class CreateTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            'owner',
            'category',
            'subject',
            'open_date',
        )

        read_only_fields = (
            'owner',
            'open_date',
        )


class CreateTicketMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = (
            'ticket',
            'message',
            'file',
            'register_date',
        )

        read_only_fields = (
            'ticket',
            'register_date',
        )
