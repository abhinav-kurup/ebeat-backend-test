from rest_framework import serializers
from .models import *


class BeatAreaDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeatAreaModel
        fields = ["name"]


class BeatAreaPolygonSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeatAreaModel
        fields = ["name", "area", "beat_no"]


class AddBOSerializer(serializers.Serializer):
    name = serializers.CharField(required = True)
    email = serializers.EmailField(required = True)
    phone = serializers.CharField(required = True)
    service_number = serializers.CharField(required = True)


class BeatOfficerModelSerializer(serializers.ModelSerializer):
    beat_area = BeatAreaDropdownSerializer()
    class Meta:
        model = BeatOfficerModel
        fields = ["email", "name", "phone", "service_number", "beat_area"]

class BeatAreaRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeatAreaModel
        fields = ["area"]

class PoliceStationModelSerializer(serializers.ModelSerializer):
    beat_areas = serializers.SerializerMethodField()
    class Meta:
        model = PoliceStationModel
        fields = ["area", "beat_areas"]
    def get_beat_areas(self, obj):
        try:
            ba = []
            ps = PoliceStationModel.objects.get(id = obj.id)
            beats = BeatAreaModel.objects.filter(region__within=ps.region)
            ser = BeatAreaRegionSerializer(beats, many=True)
            ba = ser.data
        except Exception as e:
            print(e)
        return ba

class PoliceStationNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceStationModel
        fields = ["name"]