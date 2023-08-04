from rest_framework import serializers
from .models import *


class LocationCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCategoryModel
        fields = ["id", "location_type"]


class LocationInchargeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationInchargeModel
        fields = ["name", "contact", "description"]

class LocationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationModel
        fields = ["id", "photo", "name", "address", "location"]

class LocationDetailModelSerializer(serializers.ModelSerializer):
    # last_visited = serializers.SerializerMethodField()
    incharge = serializers.SerializerMethodField()
    type = LocationCategoryModelSerializer()
    class Meta:
        model = LocationModel
        exclude = ["created_at", "updated_at", "is_active"]
    def get_incharge(self, obj):
        incahrge = None
        try:
            data = LocationInchargeModel.objects.filter(location=obj.id, is_active=True)
            serializer = LocationInchargeModelSerializer(data)
            incahrge = serializer.data
        except Exception as e:
            print(e)
        return incahrge




