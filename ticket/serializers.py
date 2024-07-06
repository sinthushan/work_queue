from rest_framework import serializers
from .models import Ticket, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields =  '__all__'


class TicketSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Ticket
        fields = [
            'id',
            'summary',
            'details',
            'status',
            'creator',
            'assigned_to',
            'completed_by',
            'created',
            'updated', 
            'team',
            'comments'
        ]
        read_only_fields =  [
            'id',
            'creator',
            'created',
            'updated',
            'comments'
        ]



