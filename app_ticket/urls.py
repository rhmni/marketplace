from django.urls import path

from app_ticket import views

app_name = 'tickets'

urlpatterns = [
    path('', views.TicketListView.as_view(), name='ticket_list'),
    path('ticket-messages/<int:ticket_id>/', views.TicketMessageListView.as_view(), name='ticket_massage_list'),
    path('tickets/create/', views.TicketCreateView.as_view(), name='create_ticket'),
    path('ticket-messages/create/<int:ticket_id>/', views.TicketMessageCreateView.as_view(), name='create_ticket_massage'),
]
