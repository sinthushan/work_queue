from rest_framework import serializers
from .models import Ticket

class GetTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class PostTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['summary', 'details', 'team']
