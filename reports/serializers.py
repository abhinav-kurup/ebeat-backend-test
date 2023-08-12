from rest_framework import serializers
from .models import *


class LoactionVisitBoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeatOfficerModel
        fields =["name"]

class LoactionVisitLocationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationModel
        fields =["name","address"]

class LoactionVisitModelSerializer(serializers.ModelSerializer):
    location = LoactionVisitLocationModelSerializer()
    class Meta:
        model = LoactionVisitModel
        fields = ["id", "location","created_at"]


class LoactionVisitDetailModelSerializer(serializers.ModelSerializer):
    location = LoactionVisitLocationModelSerializer()
    class Meta:
        model = LoactionVisitModel
        fields = ["id", "location","situation","img","audio","comments","created_at"]

class LastVisitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoactionVisitModel
        fields = ["created_at"]


# class AddLoactionVisitModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LoactionVisitModel
#         exclude = ["id","created_at","updated_at","visit_id","BO","location"]


class AddLocationVisitSerializer(serializers.Serializer):
    situation = serializers.FloatField(required = True)
    comments = serializers.CharField(required = False)
    location = serializers.CharField(required = True)
    audio = serializers.FileField(required = False)
    img = serializers.ImageField(required = False)
    def create(self, validated_data,user):
        location_visit = LoactionVisitModel.objects.create(
            BO = BeatOfficerModel.objects.get(email= user.email),
            location = LocationModel.objects.get(name = validated_data["location"]),
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
            person = PersonModel.objects.get(name = validated_data["person"]),
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
    

############################## Summon ##################

class SummonWarrentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummonWarrentModel
        fields = ["id","order_id","due_date","category"]


class SummonWarrentModelDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummonWarrentModel
        fields = ["id","order_id","name","address","due_date","category"]

############################## LOGS ##################

class BeatOfficerLogsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeatOfficerLogs
        fields = ["comment"]




################################# WEB ########################################

class WebLocationTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model= LocationCategoryModel
        fields = ["location_type"]

class WebLoactionVisitLocationModelSerializer(serializers.ModelSerializer):
    type = WebLocationTypeModelSerializer()
    class Meta:
        model = LocationModel
        fields =["name","address","type"]

class WebLoactionVisitModelSerializer(serializers.ModelSerializer):
    BO = LoactionVisitBoModelSerializer()
    location = WebLoactionVisitLocationModelSerializer()
    class Meta:
        model = LoactionVisitModel
        fields = ["id","visit_id","BO","location","created_at","situation"]

class WebLoactionVisitDetailModelSerializer(serializers.ModelSerializer):
    BO = LoactionVisitBoModelSerializer()
    location = WebLoactionVisitLocationModelSerializer()
    class Meta:
        model = LoactionVisitModel
        fields = ["id","visit_id","BO","location","situation","img","audio","comments","created_at"]
