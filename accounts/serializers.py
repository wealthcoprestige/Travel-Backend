from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()

class VerificationSerilaizer(serializers.Serializer):
    code = serializers.CharField()