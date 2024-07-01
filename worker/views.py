from django.shortcuts import render
from rest_framework import generics
from .serializers import TeamSerializer, WorkerSerializer
from .models import Team, Worker


class TeamsList(generics.ListCreateAPIView):
    queryset = Team.objects.all().order_by('team_name')
    serializer_class = TeamSerializer


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer



class WorkersList(generics.ListCreateAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

class WorkerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer