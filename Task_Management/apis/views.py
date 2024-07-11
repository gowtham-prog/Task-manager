from django.shortcuts import render
from .models import User,Task
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer,TaskSerializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

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
                user_type=serializer.validated_data['user_type']
            )
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'message':'User created successfully'},status=status.HTTP_200_OK)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserRetrieveAPIView(APIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer

    def post(self,request,*args,**kwargs):
        user =  User.objects.get(id, request.user.id)
        serializer = UserSerializer(user, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        user = request.user

        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

