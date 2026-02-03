from django.shortcuts import render
from .serializers import UserProfileSerializer, TaskSerializer
from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


from .models import Task, UserProfile, Attendence
from .permissions import IsSupervisor
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


# Create your views here.

@api_view(['POST'])
def user_register(request):
    payload = request.data
    username = payload.get('username')
    password = payload.get('password')
    role = payload.get('role')

    if not username or not password or not role:
        return Response({'detail': 'username, password and role required'}, status=status.HTTP_400_BAD_REQUEST)

    new_user = User.objects.create_user(username=username, password=password)

    serializer_data = {'user':new_user.pk,'role':role}
    serializer = UserProfileSerializer(data = serializer_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data) 
    new_user.delete()
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#Viewset view
class TaskViewSet(GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes=[IsAuthenticated]

    filterset_fields =["assigned_to__username",'status'] # /tasks/?assigned_to=1
    # filterset_fields = {
    #     "assigned_to__username": ["exact", "icontains"],
    # }
    search_fields = ["title", "assigned_to__username"]  # /tasks/?search=alice
    ordering_fields = ["created_at"]  # /tasks/?ordering=-created_at
  

    def get_permissions(self):
        if self.action in ("create",'update','partial_update', "destroy",):
            self.permission_classes = [IsSupervisor,IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def list(self, request):
        qs = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        task = self.get_object()
        task.delete()
        return Response({"message": "Task Deleted Successfully"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = Task.objects.get(id=pk)

        if task.assigned_to != request.user:
            return Response({"error": "User Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        if task.status != 'COMP':
            task.status = 'COMP'
            task.completed_at = now()
            task.save()
            return Response({"message": "Task completed"})
        return Response({"messages": "Already completed"}, status=status.HTTP_400_BAD_REQUEST)

#APIview or class-based view
#Proctected authentication
class SignInView(APIView):
    def post(self, request):
        payload = request.data
        username = payload.get('username')
        password = payload.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                return Response({'message': 'Profile not found'}, status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user)
            serializer = UserProfileSerializer(profile)
            data = serializer.data
            return Response({
                'refresh':str(refresh),
                'access':str(refresh.access_token),
                'user':data
                }
                , status=status.HTTP_200_OK)
        return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

class SignOutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist() # Adds token to the BlacklistedToken model
            return Response({"message": "Successfully signed out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

#Function based View 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_attendence(request):
    today = now().date()
    if Attendence.objects.filter(user=request.user, date=today).exists():
        return Response({"error": "Attendance already marked"}, status=400)

    Attendence.objects.create(user=request.user, date=today)
    return Response({"message": "Attendance marked"})

