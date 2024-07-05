from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PostTicketSerializer, GetTicketSerializer
from .models import Ticket
from worker.models import Worker

class AssignedTickets(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetTicketSerializer
    def get_queryset(self):
        user = self.request.user
        return user.worker.assigned_tickets.all()

class CreatedTickets(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetTicketSerializer
    def get_queryset(self):
        user = self.request.user
        return user.worker.created_tickets.all()
    
class TicketsList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetTicketSerializer
    def get_queryset(self):
        user = self.request.user
        return user.worker.team.tickets.all()


class UpdateTicket(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetTicketSerializer
    def get_queryset(self):
        user = self.request.user
        assigned_tickets =  user.worker.assigned_tickets.all()
        created_tickets =  user.worker.created_tickets.all()
        return assigned_tickets.union(created_tickets)

    def patch(self, request, *args, **kwargs):
        try:
            worker_id = request.data['worker_id']
            worker = Worker.objects.filter(id=worker_id).first()
        except KeyError:
            worker = None
        ticket_id = request.data['ticket_id']
        task = request.data['task']
        ticket = Ticket.objects.filter(id=ticket_id).first()
        ticket.update(task, worker=worker)
        serializer = GetTicketSerializer(ticket)
        return Response(serializer.data)


class CreateTicket(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostTicketSerializer
    queryset = Ticket.objects.all()


class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = GetTicketSerializer