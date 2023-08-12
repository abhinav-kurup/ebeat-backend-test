from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from base.utils import paginate
from django.db.models import Q
from authentication.permissions import *
from authentication.models import *
from .serializers import *
from .threads import *
from .models import *
import datetime



@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])       
def app_add_location_visit(request):
    try:
        data = request.data
        ser = AddLocationVisitSerializer(data=data)
        if ser.is_valid():
            location_visit = ser.create(ser.validated_data,request.user)
            location_visit.save()
            return Response({"message":"Location Report created"}, status=status.HTTP_201_CREATED)
        return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_404_NOT_FOUND)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])  
def app_get_location_visits(request):
    try:
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        queryset = LoactionVisitModel.objects.filter(BO=bo, is_active=True).order_by('-created_at')
        if request.query_params.get('location'):
            location_param = request.query_params.get('location')
            queryset = queryset.filter(location__name = location_param )
        if request.query_params.get('location_type'):
            location_type = request.query_params.get('location_type')
            queryset = queryset.filter(location__type__location_type=location_type)
        if request.query_params.get('from_date') and request.query_params.get('to_date'):
            from_date = request.query_params.get('from_date')
            to_date = request.query_params.get('to_date')
            queryset = queryset.filter(created_at__range=(from_date,to_date))     
        objs = queryset
        page = request.GET.get("page", 1)
        paginator = Paginator(objs, 6)
        data = paginate(objs, paginator, page)
        serializer = LoactionVisitModelSerializer(data["results"], many=True)
        data["results"] = serializer.data
        return Response({"data":data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["GET"])
def get_location_visit_detail(request, pk):
        try:
            if not LoactionVisitModel.objects.filter(id=pk):
                return Response({"error": "Invalid Locaiton Visit ID"}, status=status.HTTP_403_FORBIDDEN)
            queryset = LoactionVisitModel.objects.filter(id = pk)
            ser = LocationVisitDetailModelSerializer(queryset, many=True)
            return Response(ser.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])       
def app_add_person_visit(request):
    try:
        ser = AddPersonVisitSerializer(data=request.data)
        if ser.is_valid():
            person_visit = ser.create(ser.validated_data,request.user)
            person_visit.save()
            return Response({"message":"Person Report created"}, status=status.HTTP_201_CREATED)
        return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])   
def app_get_person_reports(request):
    try:
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        queryset = PersonVisitModel.objects.filter(BO = bo, is_active=True)
        if request.query_params.get('person_type'):
            person_type = request.query_params.get('person_type')
            queryset = queryset.filter(person__type__person_type=person_type)
        if request.query_params.get('from_date') and request.query_params.get('to_date'):
            from_date = request.query_params.get('from_date')
            to_date = request.query_params.get('to_date')
            queryset = queryset.filter(created_at__range=(from_date,to_date))     
        objs = queryset
        page = request.GET.get("page", 1)
        paginator = Paginator(objs, 6)
        data = paginate(objs, paginator, page)
        serializer = PersonVisitModelSerializer(data["results"], many=True)
        data["results"] = serializer.data
        return Response({"data":data}, status=status.HTTP_200_OK)
    except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])   
def get_person_report_single(request, pk):
    try:       
        if not PersonVisitModel.objects.filter(id=pk):
            return Response({"error": "Invalid Person Visit ID"}, status=status.HTTP_403_FORBIDDEN)
        queryset = PersonVisitModel.objects.filter(id = pk)
        ser = PersonVisitDetailModelSerializer(queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def app_court_order_detail(request, pk):
    try:
        if not SummonWarrentModel.objects.filter(id=pk):
            return Response({"error": "Invalid Order ID"})
        queryset = SummonWarrentModel.objects.get(order_id=pk)
        ser = SummonWarrentModelDetailSerializer(queryset)
        return Response(ser.data, status=status.HTTP_200_OK)
    except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def app_get_logs(request, dt):
    try:
        payload = {}
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        location_visits = LoactionVisitModel.objects.filter(BO = bo, created_at__date = dt)
        s1 = LoactionVisitModelSerializer(location_visits, many=True)
        person_visits = PersonVisitModel.objects.filter(BO = bo, created_at__date = dt)
        s2 = PersonVisitModelSerializer(person_visits, many=True)
        logs = BeatOfficerLogs.objects.filter(BO = bo, created_at__date = dt)
        s3 = BeatOfficerLogsModelSerializer(logs,many=True)
        payload["location_visits"] = s1.data
        payload["person_visits"] = s2.data
        payload["logs"] = s3.data
        return Response(payload, status=status.HTTP_200_OK)
    except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def app_add_logs(request):
    try:
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        ser = BeatOfficerLogsModelSerializer(data=request.data)
        if ser.is_valid():
            log = BeatOfficerLogs.objects.create(comment = ser.validated_data["comment"], BO = bo)
            log.save()
            return Response({"message":"Log Added"}, status=status.HTTP_201_CREATED)
        return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
def get_log_dates(request, mo, yr):
    try:
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        query_date = datetime(yr, mo, 1).date()    # Filter objects by month and year using the __month and __year lookups
        queryset = BeatOfficerLogs.objects.filter(created_at__month=query_date.month, created_at__year=query_date.year, BO=bo).values_list("created_at__day", flat=True)
        return Response(list(queryset), status=status.HTTP_200_OK)
    except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
