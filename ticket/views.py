from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import TicketSerializer
from .models import Ticket


class TicketsList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
   # queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    def get_queryset(self):
        user = self.request.user
        print(user.worker.team.tickets.all())
        return user.worker.team.tickets.all()



class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer