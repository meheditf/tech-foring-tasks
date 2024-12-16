from django.utils import timezone
from rest_framework import serializers
from .models import *
from users.serializers import UserSerializer

class ProjectSerializer(serializers.ModelSerializer):
    '''
    This serializer converts `Project` model instances into JSON format and validates incoming data
    to ensure it meets the requirements of the `Project` model.
    '''
    owner = UserSerializer(read_only=True)

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            raise serializers.ValidationError("Request context with a valid user is required.")
        validated_data['owner'] = request.user
        return super().create(validated_data)
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at']


class ProjectMemberSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProjectMember
        fields = ['id', 'project', 'user', 'role']


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            raise serializers.ValidationError("Request context with a valid user is required.")
        return super().create(validated_data)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority', 
            'assigned_to', 'project', 'created_at', 'due_date'
        ]


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    This serializer handles the conversion of Comment objects to and from JSON format.
    """
    user = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'task', 'created_at']
