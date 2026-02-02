from django.shortcuts import render
from .serializers import UserProfileRegisterSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['POST'])
def user_register(request):
    payload = request.data
    username = payload.get('username')
    password = payload.get('password')
    role = payload.get('role')

    if not username or not password or not role:
        return Response({'detail': 'username, password and role required'}, status=status.HTTP_400_BAD_REQUEST)

    # create user with raw password
    new_user = User.objects.create_user(username=username, password=password)

    serializer_data = {'user':new_user.pk,'role':role}
    serializer = UserProfileRegisterSerializer(data = serializer_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data) 
    new_user.delete()
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)