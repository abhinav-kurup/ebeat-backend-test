from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers_auth import *
from .serializers_main import *
from .threads import *
from .models import *


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def app_get_beat_areas(request):
    try:
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        reg = bo.police_station.area
        queryset = BeatAreaModel.objects.filter(region__within=reg, is_active=True).values_list("name", flat=True)
        return Response(list(queryset), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["GET"])
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
def app_get_beat_area_polygons(request):
    try:
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        req = bo.police_station.area
        queryset = BeatAreaModel.objects.filter(area__within=req, is_active=True)
        ser = BeatAreaPolygonSerializer(queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

