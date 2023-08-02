from rest_framework import serializers
from django.conf import settings
from .models import *


class loginSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(required = True)

class ChangePasswordSerializer(serializers.Serializer):
    old = serializers.CharField(required = True)
    new = serializers.CharField(required = True)

class otpSerializer(serializers.Serializer):
    otp = serializers.IntegerField(required = True)
    pw = serializers.CharField(required = False)

class emailSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
