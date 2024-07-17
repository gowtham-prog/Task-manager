import django.contrib
import django.core.asgi
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination

from .models import User,Task
from .serializers import UserSerializer,TaskSerializer


# Create your views here.

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def post(self,request,*args,**kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            if User.objects.filter(email=serializer.validated_data['email']).count() > 0:
                return Response(
                    {'status': 'failure', 'message': "A user with that email already exists. Use a different email."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = User.objects.create(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                # user_type=serializer.validated_data['user_type']
            )
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'message':'User created successfully'},status=status.HTTP_200_OK)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer
    # queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)



    # def post(self,request,*args,**kwargs):
    #     user =  User.objects.get(id, request.user.id)
    #     serializer = UserSerializer(user, context={'request': request})

    #     return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateAPIView(UpdateAPIView):
    def partial_update(self, request, id):
        user = request.user
        instance = get_object_or_404(User, id=id)

        if user == instance or user.user_type == "admin" or (user.user_type == "manager" and user.organization == instance.organization):
            serializer = UserSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("not updated")
            return Response({'message': 'Failure! Permission denied or user not found'}, status=status.HTTP_403_FORBIDDEN)
    # def post(self, request, *args, **kwargs):
    #     user = request.user

    #     serializer = UserSerializer(user, data=request.data, partial=True)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            RefreshToken(refresh_token).blacklist()
            return Response({'success': 'User logged out successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)


class TaskCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

class TaskListAPIView(ListAPIView):
    permission_classes = [ IsAuthenticated, ]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        user = self.request.user
        key = self.kwargs.get('key')
        if key=="assigned":
            return Task.objects.filter(assigned_to=user)
        elif key == "created":
            return Task.objects.filter(created_by=user)

class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        if request.user == self.get_object().created_by or request.user in self.get_object().assigned_to.all():
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response({'message': 'Failure! Permission denied.'}, status=status.HTTP_400_BAD_REQUEST)

        
    def partial_update(self, request, *args, **kwargs):
        user = self.request.user
        id  = self.kwargs.get('id')
        instance = Task.objects.filter(id = id).first()
        if instance.created_by == user or user in instance.assigned_to.all():
            serializer = TaskSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': 'Task altered successfully.'},status=status.HTTP_200_OK)

        else:
            return Response({'message': 'Failure! Permission denied.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_destroy(self, instance):
        if self.request.user == self.get_object().created_by or self.request.user in self.get_object().assigned_to.all():
            return instance.delete()
        else:
            return Response({'message': 'Failure! Permission denied.'}, status=status.HTTP_400_BAD_REQUEST)
