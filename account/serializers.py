from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    
# serializers.py
from rest_framework import serializers
from .models import OTPSecret

class OTPSecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPSecret
        fields = ['secret_key']
