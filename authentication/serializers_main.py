from rest_framework import serializers
from django.conf import settings
from .models import *


class BeatAreaDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeatAreaModel
        fields = ["name"]


class BeatAreaPolygonSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeatAreaModel
        fields = ["name", "region", "beat_no"]


class AddBOSerializer(serializers.Serializer):
    name = serializers.CharField(required = True)
    email = serializers.EmailField(required = True)
    phone = serializers.CharField(required = True)
    service_number = serializers.CharField(required = True)



class BeatAreaRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeatAreaModel
        fields = ["region"]

class PoliceStationModelSerializer(serializers.ModelSerializer):
    beat_areas = serializers.SerializerMethodField()
    class Meta:
        model = PoliceStationModel
        fields = ["region", "beat_areas"]
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
