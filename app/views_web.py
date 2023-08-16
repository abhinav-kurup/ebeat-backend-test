from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import request as rest_req
from rest_framework import status
from django.core.paginator import Paginator
from base.utils import paginate
from django.db.models import Q
from authentication.models import *
from .serializers import *
from .threads import *
from .models import *
from .utils import get_officer_region



@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def web_get_locations(request):
    try:
        user_obj = OfficerModel.objects.get(email=request.user.email)
        reg = get_officer_region(user_obj)
        if reg == None:
            return Response({"error": "You are not authorised to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        queryset = LocationModel.objects.filter(location__within=reg, is_active=True)
        if request.query_params.get('search'):
            search_param = request.query_params.get('search')
            filter_condition = Q(name__icontains=search_param) | Q(address__icontains=search_param)
            queryset = queryset.filter(filter_condition)
        if request.query_params.get('location_type'):
            type_param = request.query_params.get('location_type')
            queryset = queryset.filter(type__location_type=type_param)
        if request.query_params.get('beat_area'):
            area_param = request.query_params.get('beat_area')
            beat = BeatAreaModel.objects.filter(name=area_param, is_active=True).first()
            queryset = queryset.filter(location__within=beat.area, is_active=True)
        if request.query_params.get('police_station'):
            area_param = request.query_params.get('police_station')
            beat = PoliceStationModel.objects.filter(name=area_param, is_active=True).first()
            queryset = queryset.filter(location__within=beat.area, is_active=True)
        if request.query_params.get('sub_division'):
            area_param = request.query_params.get('sub_division')
            beat = SubDivisionModel.objects.filter(name=area_param, is_active=True).first()
            queryset = queryset.filter(location__within=beat.area, is_active=True)
        if request.query_params.get('district'):
            area_param = request.query_params.get('district')
            beat = DistrictModel.objects.filter(name=area_param, is_active=True).first()
            queryset = queryset.filter(location__within=beat.area, is_active=True)
        objs = queryset
        page = request.GET.get("page", 1)
        paginator = Paginator(objs, 9)
        data = paginate(objs, paginator, page)
        serializer = LocationModelSerializer(data["results"], many=True)
        data["results"] = serializer.data
        return Response({"data":data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def web_get_location_types(request):
    try:
        user_obj = OfficerModel.objects.get(email=request.user.email)
        reg = get_officer_region(user_obj)
        if reg == None:
            return Response({"error": "You are not authorised to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        queryset = LocationModel.objects.filter(location__within=reg, is_active=True).distinct('type').values_list("type__location_type", flat=True)
        return Response(list(queryset), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def web_get_previous_location_incharge(request, lo_id):
    try:
        if not LocationModel.objects.filter(id = lo_id).exists():
            return Response({"error":"Invalid Locaion ID"}, status=status.HTTP_403_FORBIDDEN)
        location_obj = LocationModel.objects.get(id=lo_id)
        ser = LocationInchargeModelSerializer(location_obj.location_incharge.filter(is_active=False), many=True)
        return Response(ser.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def web_get_people(request):
    try:
        user_obj = OfficerModel.objects.get(email=request.user.email)
        reg = get_officer_region(user_obj)
        if reg == None:
            return Response({"error": "You are not authorised to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        queryset = PersonModel.objects.filter(beat__area__within=reg)
        objs = queryset
        page = request.GET.get("page", 1)
        paginator = Paginator(objs, 9)
        data = paginate(objs, paginator, page)
        serializer = PersonModelSerializer(data["results"], many=True)
        data["results"] = serializer.data
        return Response({"data":data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

