from django.shortcuts import render
from rest_framework import generics
from .serializers import TicketSerializer
from .models import Ticket


class TicketsList(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer