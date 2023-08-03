from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework import status
from base.utils import paginate
from .serializers import *
from .threads import *
from .models import *



class GetLocationTypes(ListAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = LocationCategoryModel.objects.all()
    serializer_class = LocationCategoryModelSerializer


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
