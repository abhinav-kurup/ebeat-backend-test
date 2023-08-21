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
            if BeatAreaModel.objects.filter(area__contains = obj.location).exists():
                ser = BeatAreaDropdownSerializer(BeatAreaModel.objects.get(area__contains = obj.location))
                beat = ser.data
        except Exception as e:
            print(e)
        return beat


class PersonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationModel
        fields = ["id", "name", "address", "photo"]


class PersonDetailModelSerializer(serializers.ModelSerializer):
    last_visited = serializers.SerializerMethodField()
    # beat_area = serializers.SerializerMethodField()
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


class ApprovalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddEditLocationModel
        fields = ["name", "address", "description"]


class AppAddLocationSerializer(serializers.Serializer):
    name = serializers.CharField(required = False)
    loc_id = serializers.CharField(required = False)
    latitude = serializers.FloatField(required = False)
    longitude = serializers.FloatField(required = False)
    address = serializers.CharField(required = False)
    category = serializers.CharField(required = False)
    description = serializers.CharField(required = False)
    photo = serializers.ImageField(required = False)
    BO = serializers.UUIDField(required = False)
    incharge_name = serializers.CharField(required = False)
    incharge_contact = serializers.CharField(required = False)
    incharge_description = serializers.CharField(required = False)
    def create(self, validated_data):
        user = self.context['user']
        new_location = AddEditLocationModel.objects.create(
            approval_status = "PENDING",
            BO =  BeatOfficerModel.objects.get(email= user.email),
        )
        if 'loc_id' in validated_data:
            new_location.chaing_id = validated_data['loc_id']
        if 'name' in validated_data:
            new_location.name = validated_data['name']
        if 'latitude' in validated_data:
            new_location.latitude = validated_data['latitude']
        if 'longitude' in validated_data:
            new_location.longitude = validated_data['longitude']
        if 'category' in validated_data:
            new_location.category = validated_data['category']
        if 'description' in validated_data:
            new_location.description = validated_data['description']
        if 'address' in validated_data:
            new_location.address = validated_data['address']
        if 'photo' in validated_data:
            new_location.photo = validated_data['photo']
        if 'incharge_name' in validated_data:
            new_location.incharge_name = validated_data['incharge_name']
        if 'incharge_contact' in validated_data:
            new_location.incharge_contact = validated_data['incharge_contact']
        if 'incharge_description' in validated_data:
            new_location.incharge_description = validated_data['incharge_description']
        new_location.save()
        return new_location


class AppAddPersonSerializer(serializers.Serializer):
    name = serializers.CharField(required = False)
    person_id = serializers.CharField(required = False)
    beat = serializers.UUIDField(required = False)
    address = serializers.CharField(required = False)
    description = serializers.CharField(required = False)
    photo = serializers.ImageField(required = False)
    BO = serializers.UUIDField(required = False) 
    arm_licenses = serializers.BooleanField(required=False)
    bad_character = serializers.BooleanField(required=False)
    senior_citizen = serializers.BooleanField(required=False)
    budding_criminals = serializers.BooleanField(required=False)
    suspected_brothels = serializers.BooleanField(required=False)
    proclaimed_offenders = serializers.BooleanField(required=False)
    criminal_of_known_areas = serializers.BooleanField(required=False)
    externee_more_than_2_crimes = serializers.BooleanField(required=False)
    def create(self, validated_data):
        user = self.context['user']
        Bid =  BeatOfficerModel.objects.get(email= user.email)
        new_person = AddEditPersonModel.objects.create(
            approval_status = "PENDING",
            BO =  BeatOfficerModel.objects.get(email= user.email),
            beat = Bid.beat_area,
            # photo = validated_data['photo'],
        )
        if 'person_id' in validated_data:
            new_person.chaing_id = validated_data['person_id']
        if 'name' in validated_data:
            new_person.name = validated_data['name']
        if 'description' in validated_data:
            new_person.description = validated_data['description']
        if 'address' in validated_data:
            new_person.address = validated_data['address']
        if 'photo' in validated_data:
            new_person.photo = validated_data['photo']
        if 'bad_character' in validated_data:
            new_person.bad_character = validated_data['bad_character']
        if 'arm_licenses' in validated_data:
            new_person.arm_licenses = validated_data['arm_licenses']
        if 'senior_citizen' in validated_data:
            new_person.senior_citizen = validated_data['senior_citizen']
        if 'budding_criminals' in validated_data:
            new_person.budding_criminals = validated_data['budding_criminals']
        if 'suspected_brothels' in validated_data:
            new_person.suspected_brothels = validated_data['suspected_brothels']
        if 'proclaimed_offenders' in validated_data:
            new_person.proclaimed_offenders = validated_data['proclaimed_offenders']
        if 'criminal_of_known_areas' in validated_data:
            new_person.criminal_of_known_areas = validated_data['criminal_of_known_areas']
        if 'externee_more_than_2_crimes' in validated_data:
            new_person.externee_more_than_2_crimes = validated_data['externee_more_than_2_crimes']
        new_person.save()
        return new_person