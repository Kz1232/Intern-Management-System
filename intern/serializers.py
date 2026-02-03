from rest_framework import serializers
from .models import UserProfile ,Task
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['user','role']


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    class Meta:
        model = Task 
        fields=['title','assigned_to','status','created_at','completed_at']
