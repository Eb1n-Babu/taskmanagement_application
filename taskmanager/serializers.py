from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to', 'due_date', 'status', 'completion_report',
                  'worked_hours']
        read_only_fields = ['id', 'assigned_to']

    def validate(self, data):
        status = data.get('status')
        if status == 'completed':
            if not data.get('completion_report'):
                raise serializers.ValidationError({'completion_report': 'Required for completion.'})
            hours = data.get('worked_hours')
            if not hours or hours <= 0:
                raise serializers.ValidationError({'worked_hours': 'Must be positive.'})
        return data

    def update(self, instance, validated_data):
        if 'assigned_to' in validated_data:
            raise serializers.ValidationError("Cannot change assignee.")
        return super().update(instance, validated_data)