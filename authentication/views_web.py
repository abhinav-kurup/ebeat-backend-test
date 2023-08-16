from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from base.utils import paginate
from app.utils import *
from .serializers_auth import *
from .serializers_main import *
from .threads import *
from .models import *
from .utils import *


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def web_get_beat_officers(request):
    try:
        user_obj = OfficerModel.objects.get(email=request.user.email)
        reg = get_officer_region(user_obj)
        if reg == None:
            return Response({"error": "You are not authorised to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        queryset = BeatOfficerModel.objects.all()
        objs = queryset
        print(objs)
        page = request.GET.get("page", 1)
        paginator = Paginator(objs, 9)
        data = paginate(objs, paginator, page)
        serializer = BeatOfficerModelSerializer(data["results"], many=True)
        data["results"] = serializer.data
        return Response({"data":data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def web_add_beat_officer(request):
    try:
        user_obj = OfficerModel.objects.get(email=request.user.email)
        reg = get_officer_region(user_obj)
        if reg == None:
            return Response({"error": "You are not authorised to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        if not PoliceStationModel.objects.get(pi=user_obj):
            return Response({"error": "You are not authorised to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        ps = PoliceStationModel.objects.get(pi=user_obj)
        ser = AddBOSerializer(data=request.data)
        if ser.is_valid():
            email = ser.validated_data["email"]
            if BeatOfficerModel.objects.filter(email=email).first():
                return Response({"message":"Acount already exists."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            new_bo = BeatOfficerModel.objects.create(
                email = email,
                name = ser.validated_data["name"],
                phone = ser.validated_data["phone"],
                service_number = ser.validated_data["service_number"],
                police_station = ps,
                tid = f"BO{generate_random_string(5)}"
            )
            code = random.randint(100001, 999999)
            new_bo.set_password(str(code))
            new_bo.save()
            return Response({"message": "Beat Officer Added", "joining code": str(code)}, status=status.HTTP_201_CREATED)
        return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def web_get_beat_areas(request):
    try:
        user_obj = OfficerModel.objects.get(email=request.user.email)
        reg = get_officer_region(user_obj)
        if reg == None:
            return Response({"error": "You are not authorised to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        queryset = BeatAreaModel.objects.filter(area__within=reg, is_active=True).values_list("name", flat=True)
        return Response(list(queryset), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def web_get_beat_area_polygons(request):
    try:
        user_obj = OfficerModel.objects.get(email=request.user.email)
        reg = get_officer_region(user_obj)
        if reg == None:
            return Response({"error": "You are not authorised to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        queryset = BeatAreaModel.objects.filter(area__within=reg, is_active=True)
        ser = BeatAreaPolygonSerializer(queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
