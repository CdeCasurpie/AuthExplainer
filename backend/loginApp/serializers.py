from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password')
        return data