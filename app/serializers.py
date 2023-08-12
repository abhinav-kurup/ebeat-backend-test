from reports.serializers import LastVisitedSerializer
from rest_framework import serializers
from django.contrib.gis.geos import Point
from authentication.serializers_main import *
from authentication.models import *
from .models import *


class LocationCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCategoryModel
        fields = ["location_type"]

class PersonCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonTypeModel
        fields = ["person_type"]


class LocationInchargeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationInchargeModel
        fields = ["name", "contact", "description"]

class LocationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationModel
        fields = ["id", "photo", "name", "address", "location"]

class LocationDetailModelSerializer(serializers.ModelSerializer):
    last_visited = serializers.SerializerMethodField()
    incharge = serializers.SerializerMethodField()
    beat_area = serializers.SerializerMethodField()
    type = LocationCategoryModelSerializer()
    class Meta:
        model = LocationModel
        exclude = ["created_at", "updated_at", "is_active"]
    def get_incharge(self, obj):
        try:
            incahrge = None
            data = LocationInchargeModel.objects.filter(location=obj.id, is_active=True)
            serializer = LocationInchargeModelSerializer(data, many=True)
            incahrge = serializer.data
        except Exception as e:
            print(e)
        return incahrge
    def get_last_visited(self, obj):
        try:
            last = None
            data = obj.location_visit.order_by("-created_at").first()
            serializer = LastVisitedSerializer(data)
            last = serializer.data
        except Exception as e:
            print(e)
        return last
    def get_beat_area(self, obj):
        try:
            beat = None
            if BeatAreaModel.objects.filter(region__contains = obj.location).exists():
                ser = BeatAreaDropdownSerializer(BeatAreaModel.objects.get(region__contains = obj.location))
                beat = ser.data
        except Exception as e:
            print(e)
        return beat


class PersonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationModel
        fields = ["id", "name", "address", "location"]


class PersonDetailModelSerializer(serializers.ModelSerializer):
    last_visited = serializers.SerializerMethodField()
    beat_area = serializers.SerializerMethodField()
    type = PersonCategoryModelSerializer()
    class Meta:
        model = PersonModel
        exclude = ["created_at", "updated_at", "is_active"]
    def get_last_visited(self, obj):
        try:
            last = None
            data = obj.person_visit.order_by("-created_at").first()
            serializer = LastVisitedSerializer(data)
            last = serializer.data
        except Exception as e:
            print(e)
        return last
    def get_beat_area(self, obj):
        try:
            beat = None
            if BeatAreaModel.objects.filter(region__contains = obj.location).exists():
                ser = BeatAreaDropdownSerializer(BeatAreaModel.objects.get(region__contains = obj.location))
                beat = ser.data
        except Exception as e:
            print(e)
        return beat


class AppAddLocationSerializer(serializers.Serializer):
    name = serializers.CharField(required = True)
    latitude = serializers.FloatField(required = True)
    longitude = serializers.FloatField(required = True)
    address = serializers.CharField(required = True)
    type = serializers.CharField(required = True)
    description = serializers.CharField(required = True)
    photo = serializers.ImageField(required = True)
    incharge_name = serializers.CharField(required = True)
    incharge_contact = serializers.CharField(required = True)
    incharge_description = serializers.CharField(required = True)
    def create(self, validated_data):
        new_location = LocationModel.objects.create(
            name = validated_data["name"],
            type = LocationCategoryModel.objects.get(location_type = validated_data["type"]),
            location = Point(validated_data["longitude"],validated_data["latitude"]),
            photo = validated_data["photo"],
            address = validated_data["address"],
            description = validated_data["description"],
        )
        new_location.save()
        new_incharge = LocationInchargeModel.objects.create(
            name = validated_data["incharge_name"],
            location = new_location,
            contact = validated_data["incharge_contact"],
            description = validated_data["incharge_description"],
        )
        new_incharge.save()
        return new_location


class AppAddPersonSerializer(serializers.Serializer):
    name = serializers.CharField(required = True)
    latitude = serializers.FloatField(required = True)
    longitude = serializers.FloatField(required = True)
    address = serializers.CharField(required = True)
    type = serializers.CharField(required = True)
    description = serializers.CharField(required = True)
    photo = serializers.ImageField(required = False)
    def create(self, validated_data):
        new_person = PersonModel.objects.create(
            name = validated_data["name"],
            type = PersonTypeModel.objects.get(person_type = validated_data["type"]),
            location = Point(validated_data["longitude"],validated_data["latitude"]),
            # photo = validated_data["photo"],
            address = validated_data["address"],
            description = validated_data["description"],
        )
        if validated_data["photo"]:
            new_person.photo = validated_data["photo"]
        new_person.save()
        return new_person

