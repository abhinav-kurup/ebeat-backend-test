from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import request as rest_req
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework import status
from base.utils import paginate
from django.db.models import Q
from authentication.permissions import *
from authentication.models import *
from .serializers import *
from .threads import *
from .models import *
# from .utils import get_officer_region



# @api_view(["GET"])
# @allowed_users(["PI", "DYSP", "SP", "IGP"])
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
# def web_get_locations(request):
#     try:
        # user_obj = OfficerModel.objects.get(email=request.user.email)
        # check, region = get_officer_region(user_obj)
        # if not check:
        #     return Response({"error": "You don't have rights to access this page"}, status=status.HTTP_401_UNAUTHORIZED)
        # else:
        #     print(type(region))
        # x = StateModel.objects.first()
        # queryset = LocationModel.objects.filter(location__within=region, is_active=True)
        # if request.query_params.get('search'):
        #     search_param = request.query_params.get('search')
        #     filter_condition = Q(name__icontains=search_param) | Q(address__icontains=search_param)
        #     queryset = queryset.filter(filter_condition)
        # if request.query_params.get('location_type'):
        #     type_param = request.query_params.get('location_type')
        #     queryset = queryset.filter(type__location_type=type_param)
        # if request.query_params.get('beat_area'):
        #     area_param = request.query_params.get('beat_area')
        #     beat = BeatAreaModel.objects.filter(name=area_param, is_active=True).first()
        #     queryset = queryset.filter(location__within=beat.region, is_active=True)
        # if request.query_params.get('police_station'):
        #     area_param = request.query_params.get('police_station')
        #     beat = PoliceStationModel.objects.filter(name=area_param, is_active=True).first()
        #     queryset = queryset.filter(location__within=beat.region, is_active=True)
        # if request.query_params.get('sub_division'):
        #     area_param = request.query_params.get('sub_division')
        #     beat = SubDivisionModel.objects.filter(name=area_param, is_active=True).first()
        #     queryset = queryset.filter(location__within=beat.region, is_active=True)
        # if request.query_params.get('district'):
        #     area_param = request.query_params.get('district')
        #     beat = DistrictModel.objects.filter(name=area_param, is_active=True).first()
        #     queryset = queryset.filter(location__within=beat.region, is_active=True)
        # objs = queryset
        # page = request.GET.get("page", 1)
        # paginator = Paginator(objs, 9)
        # data = paginate(objs, paginator, page)
        # serializer = LocationModelSerializer(data["results"], many=True)
        # data["results"] = serializer.data
    #     return Response({"data":"data"}, status=status.HTTP_200_OK)
    # except Exception as e:
    #     return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def web_get_location_types(request):
    try:
        bo = OfficerModel.objects.get(email=request.user.email)
        xx = bo.police_station.region
        queryset = LocationModel.objects.filter(location__within=xx, is_active=True).distinct('type').values_list("type__location_type", flat=True)
        return Response(list(queryset), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









from guardian.shortcuts import get_objects_for_user
context = {}


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
# @allowed_users(["PI", "DYSP", "SP", "IGP"])
def test(request):
    print(request.user)
    location_data = get_objects_for_user(request.user, )
    context["message"] = "hello"
    context["locations"] = location_data
    return Response(context, status=status.HTTP_200_OK)