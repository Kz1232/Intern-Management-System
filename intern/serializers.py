from rest_framework import serializers
from .models import UserProfile
class UserProfileRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user','role']