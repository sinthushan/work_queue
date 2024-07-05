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

class CreateTicket(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostTicketSerializer
    queryset = Ticket.objects.all()

@api_view(['PATCH'])
def assign_ticket(request):
    worker_id = request.data['worker_id']
    ticket_id = request.data['ticket_id']
    worker = Worker.objects.filter(id=worker_id).first()
    ticket = Ticket.objects.filter(id=ticket_id).first()
    ticket.assign_ticket(worker)
    serializer = GetTicketSerializer(ticket)
    return Response(serializer.data)

@api_view(['PATCH'])
def close_ticket(request):
    worker_id = request.data['worker_id']
    ticket_id = request.data['ticket_id']
    worker = Worker.objects.filter(id=worker_id).first()
    ticket = Ticket.objects.filter(id=ticket_id).first()
    ticket.close_ticket(worker)
    serializer = GetTicketSerializer(ticket)
    return Response(serializer.data)

@api_view(['PATCH'])
def reject_ticket(request):
    ticket_id = request.data['ticket_id']
    ticket = Ticket.objects.filter(id=ticket_id).first()
    ticket.reject_ticket()
    serializer = GetTicketSerializer(ticket)
    return Response(serializer.data)

class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = GetTicketSerializer