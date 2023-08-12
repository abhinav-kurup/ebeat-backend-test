from rest_framework import serializers
from .models import *


class loginSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(required = True)

class ChangePasswordSerializer(serializers.Serializer):
    old = serializers.CharField(required = True)
    new = serializers.CharField(required = True)

class otpSerializer(serializers.Serializer):
    otp = serializers.IntegerField(required = True)
    password = serializers.CharField(required = True)

class emailSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)


class BeatOfficerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeatOfficerModel
        exclude = ["created_at", "updated_at"]


# class signupSerializer(serializers.Serializer):
#     name = serializers.CharField(required = True)
#     email = serializers.EmailField(required = True)
#     phone = serializers.CharField(required = True)
#     password = serializers.CharField(required = True)
#     service_id = serializers.CharField(required = False)
#     post = serializers.CharField(required = False)
#     police_station = serializers.CharField(required = False)

