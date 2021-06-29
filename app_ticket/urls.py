from django.urls import path

from app_ticket import views

app_name = 'ticket'

urlpatterns = [
    path('tickets/', views.TickectListView.as_view(), name='ticket_list'),
    path('ticket-messages/<int:ticket_id>/', views.TickectMessageListView.as_view(), name='ticket_massage_list'),
]
