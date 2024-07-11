from rest_framework import serializers
from rest_framework.generics import CreateAPIView

from .models import Task, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'username, first_name, last_name, email, password,' 
    

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

