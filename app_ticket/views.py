from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app_ticket.models import Ticket
from app_ticket.serializers import TicketSerializer, TicketMessageSerializer
from permissions import IsOwnerOrReadOnlyTicket


class TickectListView(APIView):
    """
    get list of user tickets
    """
    serializer_class = TicketSerializer

    permission_classes = (
        IsAuthenticated,
    )

    def get(self, request):
        tickets = Ticket.objects.filter(owner=request.user)
        srz_data = self.serializer_class(instance=tickets, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class TickectMessageListView(APIView):
    """
    get list of user message ticket
    """

    serializer_class = TicketMessageSerializer

    permission_classes = (
        IsOwnerOrReadOnlyTicket,
    )

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        self.check_object_permissions(request, ticket)
        ticket_messages = ticket.ticketmessages.all()
        srz_data = self.serializer_class(instance=ticket_messages, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)
