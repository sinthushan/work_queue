from django.shortcuts import render
from rest_framework import generics, status
from .serializers import TeamSerializer, WorkerSerializer
from .models import Team, Worker
from rest_framework.response import Response

class TeamsList(generics.ListCreateAPIView):
    queryset = Team.objects.all().order_by('team_name')
    serializer_class = TeamSerializer


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class CreateWorker(generics.CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = WorkerSerializer
    def post(self, request, *args, **kwargs):
        team = self.get_object()
        updated_seralizer = team.add_worker(self, request)
        if updated_seralizer is None:
             return Response({'error': 'bad stuff'},status=status.HTTP_400_BAD_REQUEST)
        return Response(updated_seralizer.data)

class WorkersList(generics.ListAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

class WorkerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer