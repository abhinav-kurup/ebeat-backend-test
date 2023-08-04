from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from .serializers import *
from .threads import *
from .models import *


payload = {}


@api_view(["POST"])
def signUp(request):
    try:
        data = request.data
        serializer = signupSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data["email"]
            if BeatOfficerModel.objects.filter(email=email).first():
                return Response({"message":"Acount already exists."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            new_customer = BeatOfficerModel.objects.create(
                email = email,
                name = serializer.data["name"],
                phone = serializer.data["phone"],
                # post = serializer.data["post"],
                service_number = serializer.data["service_id"],
                police_station = PoliceStationModel.objects.get(id = serializer.data["police_station"])
            )
            new_customer.set_password(serializer.data["password"])
            new_customer.save()
            return Response({"message":"Account created"}, status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


###################################################################################################################


@api_view(["POST"])
def bo_login(request):
    try:
        data = request.data
        serializer = loginSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data["email"]
            password = serializer.data["password"]
            if not BeatOfficerModel.objects.filter(email=email).exists():
                return Response({"error":"Account does not exist"}, status=status.HTTP_404_NOT_FOUND)
            user = authenticate(email=email, password=password)
            if not user:
                return Response({"error":"Incorrect password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            jwt_token = RefreshToken.for_user(user)
            payload["message"] = "Login Successfull"
            payload["boid"] = user.id
            payload["token"] = str(jwt_token.access_token)
            return Response(payload, status=status.HTTP_202_ACCEPTED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def bo_forgot(request):
    try:
        data = request.data
        serializer = emailSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data["email"]
            if not BeatOfficerModel.objects.filter(email=email).exists():
                return Response({"errror": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
            thread_obj = SendForgotOTP(email)
            thread_obj.start()
            return Response({"message":"Reset Mail Sent"}, status=status.HTTP_200_OK)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def bo_reset(request):
    try:
        data = request.data
        serializer = otpSerializer(data=data)
        if serializer.is_valid():
            otp = serializer.data["otp"]
            cached_email = cache.get(otp)
            if not cached_email:
                return Response({"error":"OTP expired"}, status=status.HTTP_408_REQUEST_TIMEOUT)
            if not BeatOfficerModel.objects.filter(email=cached_email).first():
                return Response({"error":"User does not Exist"}, status=status.HTTP_404_NOT_FOUND)
            user_obj = BeatOfficerModel.objects.get(email=cached_email)
            user_obj.set_password(serializer.data["password"])
            user_obj.save()
            cache.delete(otp)
            return Response({"message":"Password Changed Successfull"}, status=status.HTTP_202_ACCEPTED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


###################################################################################################################



@api_view(["POST"])
def officer_login(request):
    try:
        data = request.data
        serializer = loginSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data["email"]
            password = serializer.data["password"]
            if not OfficerModel.objects.filter(email=email).exists():
                return Response({"error":"Account does not exist"}, status=status.HTTP_404_NOT_FOUND)
            user = authenticate(email=email, password=password)
            if not user:
                return Response({"error":"Incorrect password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            jwt_token = RefreshToken.for_user(user)
            tok = str(jwt_token.access_token)
            response = Response({"message": "Login Successfull"})
            response.set_cookie("tok", tok, httponly=True, expires=(datetime.now() + timedelta(hours=9)))
            return response
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def officer_forgot(request):
    try:
        data = request.data
        serializer = emailSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data["email"]
            if not OfficerModel.objects.filter(email=email).exists():
                return Response({"errror": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
            thread_obj = SendForgotOTP(email)
            thread_obj.start()
            return Response({"message":"Reset Mail Sent"}, status=status.HTTP_200_OK)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def officer_reset(request):
    try:
        data = request.data
        serializer = otpSerializer(data=data)
        if serializer.is_valid():
            otp = serializer.data["otp"]
            cached_email = cache.get(otp)
            if not cached_email:
                return Response({"error":"OTP expired"}, status=status.HTTP_408_REQUEST_TIMEOUT)
            if not OfficerModel.objects.filter(email=cached_email).first():
                return Response({"error":"User does not Exist"}, status=status.HTTP_404_NOT_FOUND)
            user_obj = OfficerModel.objects.get(email=cached_email)
            user_obj.set_password(serializer.data["password"])
            user_obj.save()
            cache.delete(otp)
            return Response({"message":"Password Changed Successfull"}, status=status.HTTP_202_ACCEPTED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetBeatAreaDropdown(ListAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = BeatAreaModel.objects.all()
    serializer_class = BeatAreaDropdownSerializer
