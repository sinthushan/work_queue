from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TeamSerializer, WorkerSerializer
from .models import Team, Worker


class TeamsView(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by('team_name')
    serializer_class = TeamSerializer


class WorkersView(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
