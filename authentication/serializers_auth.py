from rest_framework import serializers
from .serializers_main import *
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
    beat_area = BeatAreaDropdownSerializer()
    police_station = PoliceStationNameSerializer()
    class Meta:
        model = BeatOfficerModel
        fields = ["name", "email", "phone", "profile_pic", "service_number", "dob", "tid", "police_station", "beat_area"]


class BOPersonalDetails(serializers.Serializer):
    name = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    address = serializers.CharField(required = True)
    profile_pic = serializers.ImageField(required = True)
    dob = serializers.DateField(required = True)
