from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework import status
from base.utils import paginate
from authentication.permissions import *
from authentication.models import *
from .serializers import *
from .threads import *
from .models import *


# @api_view(["GET"])
class GetLocationTypes(ListAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = LocationCategoryModel.objects.all()
    serializer_class = LocationCategoryModelSerializer


@api_view(["GET"])
@permission_classes([IsBO])
def app_get_locations(request):
    try:
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        region = bo.police_station.region
        queryset = LocationModel.objects.filter(location__within=region, is_active=True)
        if request.query_params.get('search'):
            search_param = request.query_params.get('search')
            objs = queryset.filter(name__icontains=search_param, address__icontains=search_param)
        else:
            objs = queryset
        page = request.GET.get("page", 1)
        paginator = Paginator(objs, 6)
        data = paginate(objs, paginator, page)
        serializer = LocationModelSerializer(data["results"], many=True)
        data["results"] = serializer.data
        return Response({"data":data}, status=status.HTTP_200_OK)
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


