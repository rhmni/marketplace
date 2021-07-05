from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app_ticket.models import Ticket
from app_ticket import serializers
from permissions import IsOwnerOfTicket


class TicketListView(GenericAPIView):
    """
        get list of user tickets
    """
    serializer_class = serializers.TicketSerializer

    permission_classes = (
        IsAuthenticated,
    )

    def get(self, request):
        tickets = Ticket.objects.filter(owner=request.user)
        srz_data = self.serializer_class(instance=tickets, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class TicketMessageListView(GenericAPIView):
    """
        get list of user message ticket
    """

    serializer_class = serializers.TicketMessageSerializer

    permission_classes = (
        IsOwnerOfTicket,
    )

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        self.check_object_permissions(request, ticket)
        ticket_messages = ticket.ticketmessages.all()
        srz_data = self.serializer_class(instance=ticket_messages, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class TicketCreateView(APIView):
    """
        create new ticket
    """

    serializer_class = serializers.CreateTicketSerializer

    permission_classes = (
        IsAuthenticated,
    )

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            srz_data.save(
                owner=request.user,
                open_date=datetime.now(),
            )
            return Response({'message': 'ticket created.'}, status=status.HTTP_201_CREATED)


class TicketMessageCreateView(APIView):
    """
        create new ticket message
    """

    serializer_class = serializers.CreateTicketMessageSerializer

    permission_classes = (
        IsOwnerOfTicket,
    )

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        if ticket.is_open:
            self.check_object_permissions(request, ticket)
            srz_data = self.serializer_class(data=request.data)
            if srz_data.is_valid(raise_exception=True):
                srz_data.save(
                    ticket=ticket,
                    register_date=datetime.now(),
                )
                return Response({'message': 'ticket message created.'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'this ticket is already closed, open a new'}, status=status.HTTP_400_BAD_REQUEST)
