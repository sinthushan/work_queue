from django.shortcuts import render
from rest_framework import generics,permissions, status
from .serializers import TeamSerializer, WorkerSerializer
from .models import Team, Worker
from rest_framework.response import Response
from .permissions import CanAddWorker


class TeamsList(generics.ListCreateAPIView):
    queryset = Team.objects.all().order_by('team_name')
    serializer_class = TeamSerializer


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class CreateWorker(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, CanAddWorker]
    queryset = Team.objects.all()
    serializer_class = WorkerSerializer
    def post(self, request, *args, **kwargs):
        team = self.get_object()
        updated_seralizer = team.add_worker(self, request)
        if 'error' in  updated_seralizer:
             return Response(updated_seralizer,status=status.HTTP_400_BAD_REQUEST)
        return Response(updated_seralizer.data)

class WorkersList(generics.ListAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

class WorkerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer