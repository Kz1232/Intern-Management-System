from rest_framework import serializers
from .models import UserProfile ,Task
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['user','role']


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ['id','assigned_to' ,'title', 'status', 'created_at','completed_at']
        

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','title','status','created_at', 'completed_at']
        read_only_fields = ['created_at', 'completed_at']