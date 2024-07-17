from rest_framework import serializers
from rest_framework.generics import CreateAPIView

from .models import Task, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'first_name', 'last_name', 'email', 'password', 'user_type', 'organization') 
        read_only_fields = ['user_type']
    

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['created_by'] = UserSerializer(instance.created_by, many=False, allow_null=True, required=False).data
        data['assigned_to'] = UserSerializer(instance.assigned_to, many=True, allow_null=True, required=False).data
        
        return data

