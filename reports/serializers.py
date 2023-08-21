from rest_framework import serializers
from .models import *


class LastVisitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoactionVisitModel
        fields = ["created_at"]


class AddLocationVisitSerializer(serializers.Serializer):
    situation = serializers.FloatField(required = True)
    comments = serializers.CharField(required = False)
    location = serializers.CharField(required = True)
    audio = serializers.FileField(required = False)
    img = serializers.ImageField(required = False)
    def create(self, validated_data,user):
        location_visit = LoactionVisitModel.objects.create(
            BO = BeatOfficerModel.objects.get(email= user.email),
            location = LocationModel.objects.get(id = validated_data["location"]),
            situation = validated_data["situation"],
        )
        if validated_data["img"]:
            location_visit.img = validated_data["img"]
        if validated_data["audio"]:
            location_visit.audio = validated_data["audio"]
        if validated_data["comments"]:
            location_visit.comments = validated_data["comments"]
        location_visit.save()
        return location_visit


class AddOfflineLocationVisitSerializer(serializers.Serializer):
    situation = serializers.FloatField(required = True)
    comments = serializers.CharField(required = False)
    location = serializers.CharField(required = True)
    created_at = serializers.DateTimeField(required = True)
    audio = serializers.FileField(required = False)
    img = serializers.ImageField(required = False)
    def create(self, validated_data,user):
        location_visit = LoactionVisitModel.objects.create(
            BO = BeatOfficerModel.objects.get(email= user.email),
            location = LocationModel.objects.get(id = validated_data["location"]),
            situation = validated_data["situation"],
        )
        if validated_data["created_at"]:
            location_visit.created_at = validated_data["created_at"]
        if validated_data["img"]:
            location_visit.img = validated_data["img"]
        if validated_data["audio"]:
            location_visit.audio = validated_data["audio"]
        if validated_data["comments"]:
            location_visit.comments = validated_data["comments"]
        location_visit.save()
        return location_visit

class LoactionVisitLocationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationModel
        fields =["name", "address"]

class LoactionVisitModelSerializer(serializers.ModelSerializer):
    location = LoactionVisitLocationModelSerializer()
    class Meta:
        model = LoactionVisitModel
        fields = ["id", "location", "created_at", "situation"]


class LocationVisitDetailModelSerializer(serializers.ModelSerializer):
    location = LoactionVisitLocationModelSerializer()
    class Meta:
        model = LoactionVisitModel
        fields = ["id", "location","situation","img","audio","comments","created_at"]



class PersonVisitPersonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonModel
        fields =["name","address"]

class PersonVisitModelSerializer(serializers.ModelSerializer):
    # BO = LoactionVisitBoModelSerializer()
    person = PersonVisitPersonModelSerializer()
    class Meta:
        model = LoactionVisitModel
        fields = ["id", "person","created_at"]

class PersonVisitDetailModelSerializer(serializers.ModelSerializer):
    # BO = LoactionVisitBoModelSerializer()
    person = PersonVisitPersonModelSerializer()
    class Meta:
        model = LoactionVisitModel
        fields = ["id", "person","img","comments","audio","created_at","situation"]


class AddPersonVisitSerializer(serializers.Serializer):
    situation = serializers.FloatField(required = True)
    comments = serializers.CharField(required = False)
    person = serializers.CharField(required = True)
    audio = serializers.FileField(required = False)
    img = serializers.ImageField(required = False)
    def create(self, validated_data,user):
        person_visit = PersonVisitModel.objects.create(
            BO = BeatOfficerModel.objects.get(email= user.email),
            person = PersonModel.objects.get(id = validated_data["person"]),
            situation = validated_data["situation"],
        )
        if validated_data["img"]:
            person_visit.img = validated_data["img"]
        if validated_data["audio"]:
            person_visit.audio = validated_data["audio"]
        if validated_data["comments"]:
            person_visit.comments = validated_data["comments"]
        person_visit.save()
        return person_visit
    
class CourtOrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtOrderModel
        fields = ["id","order_id","category","due_date"]

class CourtOrderChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtOrderModel
        fields = ["order_status","comment","visted_at","photo"]
    def update(self, instance, validated_data):
        instance.order_status = validated_data["order_status"]
        instance.photo = validated_data["photo"]
        instance.comment = validated_data["comment"]
        instance.visted_at = datetime.now()
        instance.save()
        return instance


class CourtOrderModelDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtOrderModel
        fields = ["order_id", "order_name", "address", "due_date", "category"]


class BeatOfficerLogsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeatOfficerLogs
        fields = ["comment"]
