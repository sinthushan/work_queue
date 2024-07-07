from rest_framework import serializers
from .models import Team, Worker, User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'email']
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

class WorkerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=False)
    class Meta:
        model = Worker
        fields = ['user', 'position_type', 'work_hours']

class TeamSerializer(serializers.ModelSerializer):
    workers = WorkerSerializer(many=True, read_only=True)
    class Meta:
        model = Team
        fields = ['team_name', 'workers']




