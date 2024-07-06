from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TicketSerializer, CommentSerializer
from .models import Ticket
from .permissions import IsCreatorAsignee
from worker.models import Worker

class AssignedTickets(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketSerializer
    def get_queryset(self):
        user = self.request.user
        return user.worker.assigned_tickets.all()

class CreatedTickets(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketSerializer
    def get_queryset(self):
        user = self.request.user
        return user.worker.created_tickets.all()
    
class TicketsList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketSerializer
    def get_queryset(self):
        user = self.request.user
        return user.worker.team.tickets.all()


class UpdateTicket(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCreatorAsignee]
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def patch(self, request, *args, **kwargs):
        ticket = self.get_object()
        updated_seralizer = ticket.update(self, request)
        return Response(updated_seralizer.data)

class AddComment(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCreatorAsignee]
    serializer_class = CommentSerializer
    queryset = Ticket.objects.all()

    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        updated_seralizer = ticket.add_comment(self, request)
        return Response(updated_seralizer.data)


class CreateTicket(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    
    def post(self, request, *args, **kwargs):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['creator'] = request.user.worker
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer