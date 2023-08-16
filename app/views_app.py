from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from base.utils import paginate
from django.db.models import Q
from authentication.models import *
from .serializers import *
from .threads import *
from .models import *



@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def app_get_location_types(request):
    try:
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        reg = bo.police_station.area
        queryset = LocationModel.objects.filter(location__within=reg, is_active=True).distinct('type').values_list("type__location_type", flat=True)
        return Response(list(queryset), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def app_get_locations(request):
    try:
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        reg = bo.police_station.area
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
            beat = BeatAreaModel.objects.filter(name=area_param).first()
            queryset = queryset.filter(location__within=beat.region, is_active=True)
        objs = queryset
        page = request.GET.get("page", 1)
        paginator = Paginator(objs, 6)
        data = paginate(objs, paginator, page)
        serializer = LocationModelSerializer(data["results"], many=True)
        data["results"] = serializer.data
        return Response({"data":data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SingleLocationView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = LocationModel.objects.all()
    serializer_class = LocationDetailModelSerializer
    lookup_field = "id"


######################################################################################################################################################


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def app_get_people(request):
    try:
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        region = bo.police_station.region
        queryset = PersonModel.objects.filter(location__within=region, is_active=True)
        if request.query_params.get('search'):
            search_param = request.query_params.get('search')
            filter_condition = Q(name__icontains=search_param) | Q(address__icontains=search_param)
            queryset = queryset.filter(filter_condition)
        if request.query_params.get('person_type'):
            type_param = request.query_params.get('person_type')
            queryset = queryset.filter(type__person_type=type_param)
        if request.query_params.get('beat_area'):
            area_param = request.query_params.get('beat_area')
            beat = BeatAreaModel.objects.filter(name=area_param).first()
            queryset = queryset.filter(location__within=beat.region, is_active=True)
        objs = queryset
        page = request.GET.get("page", 1)
        paginator = Paginator(objs, 6)
        data = paginate(objs, paginator, page)
        serializer = LocationModelSerializer(data["results"], many=True)
        data["results"] = serializer.data
        return Response({"data":data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SinglePersonView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PersonModel.objects.all()
    serializer_class = PersonDetailModelSerializer
    lookup_field = "id"


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@api_view(["POST"])
def app_add_person(request):
    try:
        data = request.data
        ser = AppAddPersonSerializer(data=data)
        if ser.is_valid():
            ser.save()
            return Response({"message":"Person Added"}, status=status.HTTP_201_CREATED)
        return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
