from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework import status
from base.utils import paginate
from django.db.models import Q
from authentication.permissions import *
from authentication.models import *
from authentication.serializers import *
from authentication.decorators import *
from django.shortcuts import get_object_or_404
from reports.models import *
from reports.serializers import *
from base.models import BasePolygon
from .serializers import *
from .threads import *
from .models import *
from django.contrib.gis.geos import Point


# @api_view(["GET"])
class GetLocationTypes(ListAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = LocationCategoryModel.objects.all()
    serializer_class = LocationCategoryModelSerializer

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_locations(request):
    try:
        data = request.data
        serializer = AddLocationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Account created"}, status=status.HTTP_201_CREATED)
        else:    
            return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def update_location(request,pk):
        try:
            try:
                location = LocationModel.objects.get(pk=pk)
            except LocationModel.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            data = request.data
            serializer = UpdateLocationSerializer(location,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Updated Location"}, status=status.HTTP_201_CREATED)
            else:    
                return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def app_get_locations(request):
    try:
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        region1 = bo.police_station.region
        queryset = LocationModel.objects.filter(location__within=region1, is_active=True)
        print(queryset)
        if request.query_params.get('search'):
            search_param = request.query_params.get('search')
            filter_condition = Q(name__icontains=search_param) | Q(address__icontains=search_param)
            queryset = queryset.filter(filter_condition)
        if request.query_params.get('location_type'):
            location_type = request.query_params.get('location_type')
            queryset = queryset.filter(type__location_type=location_type)
        if request.query_params.get('beat_area'):
            beat_area = request.query_params.get('beat_area')
            b_a = BeatAreaModel.objects.get(name=beat_area)
            beatarea =b_a.region
            queryset = queryset.filter(location__within=beatarea, is_active=True)
        # else:
        objs = queryset
        page = request.GET.get("page", 1)
        paginator = Paginator(objs, 6)
        data = paginate(objs, paginator, page)
        serializer = LocationModelSerializer(data["results"], many=True)
        data["results"] = serializer.data
        return Response({"data":data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def app_get_location_types(request):
    try:
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        region = bo.police_station.region
        queryset = LocationModel.objects.filter(location__within=region, is_active=True).distinct('type').values_list("type__location_type", flat=True)
        return Response(list(queryset), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LocationModelListView(ListAPIView):
    queryset = LocationModel.objects.filter(is_active=True).order_by("-created_at")
    serializer_class = LocationModelSerializer
    def list(self, request):
        try:
            objs = self.queryset
            page = request.GET.get("page", 1)
            paginator = Paginator(objs, 6)
            data = paginate(objs, paginator, page)
            serializer = self.serializer_class(data["results"], many=True)
            data["results"] = serializer.data
            return Response({"data":data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SingleLocationView(RetrieveAPIView):
    queryset = LocationModel.objects.all()
    serializer_class = LocationDetailModelSerializer
    lookup_field = "id"


#################################  PERSON   #######################################
@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def app_get_person(request):
    if request.user.is_authenticated:
        try:
            bo = BeatOfficerModel.objects.get(email=request.user.email)
            region1 = bo.police_station.region
            queryset = PersonModel.objects.filter(location__within=region1, is_active=True)
            if request.query_params.get('search'):
                search_param = request.query_params.get('search')
                filter_condition = Q(name__icontains=search_param) | Q(address__icontains=search_param)
                queryset = queryset.filter(filter_condition)
            if request.query_params.get('person_type'):
                person_type = request.query_params.get('person_type')
                queryset = queryset.filter(type__person_type=person_type)
            if request.query_params.get('beat_area'):
                beat_area = request.query_params.get('beat_area') 
                print(beat_area)
                b_a = BeatAreaModel.objects.get(name=beat_area)
                beatarea =b_a.region
                print(beatarea)
                queryset = queryset.filter( location__within =beatarea,is_active=True)
                print(queryset)
            objs = queryset
            page = request.GET.get("page", 1)
            paginator = Paginator(objs, 6)
            data = paginate(objs, paginator, page)
            serializer = PersonModelSerializer(data["results"], many=True)
            data["results"] = serializer.data
            return Response({"data":data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def app_get_person_types(request):
    try:
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        region = bo.police_station.region
        queryset = PersonModel.objects.filter(location__within=region, is_active=True).distinct('type').values_list("type__person_type", flat=True)
        return Response(list(queryset), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SinglePersonView(RetrieveAPIView):
    queryset = PersonModel.objects.all()
    serializer_class = PersonDetailModelSerializer
    lookup_field = "id"




        


################################################## REPORTS #######################################################################
from reports.models import *
from reports.serializers import *

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])       
def add_location_reports(request):
    try:
        data = request.data
        serializer = AddLocationVisitSerializer(data=data)
        if serializer.is_valid():
            location_visit = serializer.create(serializer.validated_data,request.user)
            location_visit.save()
            return Response({"message":"Location Report created"}, status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def get_location_reports(request):
    if request.user.is_authenticated:
        try:
            bo = BeatOfficerModel.objects.get(email=request.user.email)
            region1 = bo.police_station.region
            id_list = LocationModel.objects.filter(location__within=region1, is_active=True).values_list('id', flat=True)
            queryset = LoactionVisitModel.objects.filter(location__in =id_list,BO = request.user.id).order_by('created_at')
            if request.query_params.get('location'):
                search_param = request.query_params.get('location')
                # id = LocationModel.objects.get(name = search_param)
                # filter_condition = Q(name__icontains=search_param) | Q(address__icontains=search_param)
                queryset = queryset.filter(location__name = search_param )
            if request.query_params.get('location_type'):
                location_type = request.query_params.get('location_type')
                # id = LocationModel.objects.filter(type__location_type=location_type)
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
def get_location_detail_reports(request):
    if request.user.is_authenticated:
        try:
            
            id = request.query_params.get('id')
            queryset = LoactionVisitModel.objects.filter(id =id,BO = request.user.id)
            objs = queryset
            page = request.GET.get("page", 1)
            paginator = Paginator(objs, 6)
            data = paginate(objs, paginator, page)
            serializer = LoactionVisitDetailModelSerializer(data["results"], many=True)
            data["results"] = serializer.data
            return Response({"data":data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])       
def add_person_reports(request):
    try:
        data = request.data
        print(request.user.id)
        serializer = AddPersonVisitSerializer(data=data)
        if serializer.is_valid():
            person_visit = serializer.create(serializer.validated_data,request.user)
            person_visit.save()
            return Response({"message":"Person Report created"}, status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_person_reports(request):
    if request.user.is_authenticated:
        try:
            bo = BeatOfficerModel.objects.get(email=request.user.email)
            region1 = bo.police_station.region
            id_list = PersonModel.objects.filter(location__within=region1, is_active=True).values_list('id', flat=True)
            queryset = PersonVisitModel.objects.filter(person__in =id_list,BO = request.user.id)
            if request.query_params.get('person_type'):
                print("nnnn")
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
def get_person_detail_reports(request):
    if request.user.is_authenticated:
        try:       
            if  request.query_params.get('id'):
                id=request.query_params.get('id')
                print(id)
                if PersonVisitModel.objects.filter(id =id,BO = request.user.id):
                    queryset = PersonVisitModel.objects.filter(id =id,BO = request.user.id)
                    objs = queryset
                    page = request.GET.get("page", 1)
                    paginator = Paginator(objs, 6)
                    data = paginate(objs, paginator, page)
                    serializer = PersonVisitDetailModelSerializer(data["results"], many=True)
                    data["results"] = serializer.data
                return Response({"data":data}, status=status.HTTP_200_OK)
            else:
                return Response({"data":"No data"})
        except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


        ############################# SUMMONS & WARRANTS #############################################################

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def app_get_summons(request):
    try:
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        serializer1 = BeatOfficerProfileSerializer(bo)
        if SummonWarrentModel.objects.filter(assigned_to__email=request.user.email, is_visited=False):
            summons = SummonWarrentModel.objects.filter(assigned_to__email=request.user.email, is_visited=False)
            page = request.GET.get("page", 1)
            paginator = Paginator(summons, 6)
            data = paginate(summons, paginator, page)
            serializer = SummonWarrentModelSerializer(data["results"], many=True)
            data["results"] = serializer.data
            return Response({"data":data,"officer_info":serializer1.data}, status=status.HTTP_200_OK)
        return Response({"data":serializer1.data}, status=status.HTTP_200_OK)

    except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def app_summons_details(request):
    try:
        
        if request.query_params.get('id'):
            id = request.query_params.get('id')
            summons = SummonWarrentModel.objects.filter( order_id=id)
            serializer = SummonWarrentModelDetailSerializer(summons, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        else:

            return Response({"data":"no data"}, status=status.HTTP_200_OK)

    except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


############################# LOGS #############################################################

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def app_get_logs(request):
    try:
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        serializer1 = BeatOfficerProfileSerializer(bo)
        if request.query_params.get('date'):
            date = request.query_params.get('date')
            location = LoactionVisitModel.objects.filter(BO__email=request.user.email,created_at__date = date)
            # page = request.GET.get("page", 1)
            # paginator = Paginator(summons, 6)
            # data = paginate(summons, paginator, page)
            serializer = LoactionVisitModelSerializer(location,many=True)
            person = PersonVisitModel.objects.filter(BO__email=request.user.email,created_at__date=date)
            person_serializer = PersonVisitModelSerializer(person,many=True)
            logs = BeatOfficerLogs.objects.filter(BO__email=request.user.email,created_at__date=date)
            log_serializer = BeatOfficerLogsModelSerializer(logs,many=True)
            return Response({"Log":log_serializer.data,"location":serializer.data,"person":person_serializer.data}, status=status.HTTP_200_OK)
        return Response({"data":serializer1.data}, status=status.HTTP_200_OK)

    except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def app_add_logs(request):
    try:
        serializer = BeatOfficerLogsModelSerializer(data=request.data)
        if serializer.is_valid():
            log = BeatOfficerLogs.objects.create(
                comment = serializer.data["comment"],
                BO =  BeatOfficerModel.objects.get(email = request.user.email)
            )
            log.save()
            return Response({"message":"Account created"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_log_dates(request):
    try:
        if request.query_params.get('month') and request.query_params.get('year'):
            month_param = request.GET.get('month')
            year_param = request.GET.get('year')
            month = int(month_param)
            year = int(year_param)
            query_date = datetime(year, month, 1).date()
            
            # Filter objects by month and year using the __month and __year lookups
            queryset = BeatOfficerLogs.objects.filter(created_at__month=query_date.month,created_at__year=query_date.year,BO__email=request.user.email).values_list("created_at", flat=True)
            data = [obj.strftime('%Y-%m-%d') for obj in queryset]
            return Response(list(data), status=status.HTTP_200_OK)
        else:
            return Response({"error":"No parameters"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
##################################### WEB ###############################################

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
def web_get_location_types(request):
    try:
        queryset = LocationModel.objects.filter( is_active=True).distinct('type').values_list("type__location_type", flat=True)
        return Response(list(queryset), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["GET"])
#@allowed_users(allowed_roles=['SP','PI'])
#@permission_classes([IsBO])
def web_get_locations(request):
    try:
        # bo = BeatOfficerModel.objects.get(email=request.user.email)
        # region1 = bo.police_station.region
        queryset = LocationModel.objects.filter( is_active=True)
        # location_type = request.query_params.getList('locationType[]')
        # print(location_type)
        # if request.query_params.get('search'):
        #     search_param = request.query_params.get('search')
        #     filter_condition = Q(name__icontains=search_param) | Q(address__icontains=search_param)
        #     queryset = queryset.filter(filter_condition)
        if request.query_params.get('locationType'):
            location_types = request.query_params.getlist('locationType')
            li = location_types
            print("@@@@@@@@@@@@@@@@@@@@@@")
            queryset = LocationModel.objects.filter(type__location_type__in=li)
            # location_type = request.query_params.get('locationType')
            # location_type = request.get.getList('location_type[]')
            # print(location_type)
            # queryset = queryset.filter(type__location_type=location_type)
        # if request.query_params.get('beat_area'):
        #     beat_area = request.query_params.get('beat_area')
        #     b_a = BeatAreaModel.objects.get(name=beat_area)
        #     beatarea =b_a.region
        #     queryset = queryset.filter(location__within=beatarea, is_active=True)
        # else:
        objs = queryset
        page = request.GET.get("page", 1)
        paginator = Paginator(objs, 6)
        data = paginate(objs, paginator, page)
        serializer = LocationDetailModelSerializer(data["results"], many=True)
        data["results"] = serializer.data
        return Response({"data":data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(["GET"])
def web_location_detail(request):
    try:       
        if request.query_params.get('id'):
            id = request.query_params.get('id')
            location = LocationModel.objects.filter( id=id)
            serializer = LocationDetailModelSerializer(location, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#####   WEB Reports

@api_view(["GET"])
def web_location_reports(request):
        try:
            id_list = LocationModel.objects.filter( is_active=True).values_list('id', flat=True)
            print(id_list)
            queryset = LoactionVisitModel.objects.filter(location__in =id_list).order_by('created_at')
            if request.query_params.get('location'):
                search_param = request.query_params.get('location')
                # id = LocationModel.objects.get(name = search_param)
                # filter_condition = Q(name__icontains=search_param) | Q(address__icontains=search_param)
                queryset = queryset.filter(location__name = search_param )
            if request.query_params.get('locationType'):
                location_type = request.query_params.get('locationType')
                # id = LocationModel.objects.filter(type__location_type=location_type)
                queryset = queryset.filter(location__type__location_type=location_type)
            if request.query_params.get('from_date') and request.query_params.get('to_date'):
                from_date = request.query_params.get('from_date')
                to_date = request.query_params.get('to_date')
                queryset = queryset.filter(created_at__range=(from_date,to_date))   
            if request.query_params.get('beat_area'):
                beat_area = request.query_params.get('beat_area')
                b_a = BeatAreaModel.objects.get(name=beat_area)
                beatarea =b_a.region
                queryset = queryset.filter(location__location__within=beatarea, is_active=True)  
            objs = queryset
            page = request.GET.get("page", 1)
            paginator = Paginator(objs, 6)
            data = paginate(objs, paginator, page)
            serializer = WebLoactionVisitModelSerializer(data["results"], many=True)
            data["results"] = serializer.data
            return Response({"data":data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(["GET"])
def web_location_report_detail(request):
    try:       
        if request.query_params.get('id'):
            id = request.query_params.get('id')
            location = LoactionVisitModel.objects.filter( id=id)
            serializer = WebLoactionVisitDetailModelSerializer(location, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["GET"])
def web_get_location_types(request):
    try:
        queryset = LocationModel.objects.filter(is_active=True).distinct('type').values_list("type__location_type", flat=True)
        return Response(list(queryset), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def web_get_location_names(request):
    try:
        queryset = LocationModel.objects.filter(is_active=True).distinct('type').values_list("name", flat=True)
        return Response(list(queryset), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["GET"])
def app_get_beat_areas(request):
    try:
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        region = bo.police_station.region
        queryset = BeatAreaModel.objects.filter(region__within=region, is_active=True).values_list("name", flat=True)
        return Response(list(queryset), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["GET"])
def web_get_person(request):
    if request.user.is_authenticated:
        try:
            # bo = BeatOfficerModel.objects.get(email=request.user.email)
            # region1 = bo.police_station.region
            queryset = PersonModel.objects.filter( is_active=True)
            if request.query_params.get('search'):
                search_param = request.query_params.get('search')
                filter_condition = Q(name__icontains=search_param) | Q(address__icontains=search_param)
                queryset = queryset.filter(filter_condition)
            if request.query_params.get('person_type'):
                person_type = request.query_params.get('person_type')
                queryset = queryset.filter(type__person_type=person_type)
            if request.query_params.get('beat_area'):
                beat_area = request.query_params.get('beat_area') 
                print(beat_area)
                b_a = BeatAreaModel.objects.get(name=beat_area)
                beatarea =b_a.region
                print(beatarea)
                queryset = queryset.filter( location__within =beatarea,is_active=True)
                print(queryset)
            objs = queryset
            page = request.GET.get("page", 1)
            paginator = Paginator(objs, 6)
            data = paginate(objs, paginator, page)
            serializer = PersonModelSerializer(data["results"], many=True)
            data["results"] = serializer.data
            return Response({"data":data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



######################## Testing ####################################

@api_view(["GET"])
def get_region(request):
    ps = PoliceStationModel.objects.first()
    ser = PoliceRegionSerializer(ps)
    reg = ps.region
    queryset = BeatAreaModel.objects.filter(region__within=reg)
    serializer = RegionSerializer(queryset , many=True)
    return Response({"police station":ser.data,"beat area":serializer.data}, status=status.HTTP_200_OK)