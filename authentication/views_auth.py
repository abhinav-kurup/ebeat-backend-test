# from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers_auth import *
from .threads import *
from .models import *


###################################################################################################################


@api_view(["POST"])
def bo_login(request):
    try:
        data = request.data
        serializer = loginSerializer(data=data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            bo = BeatOfficerModel.objects.get(email=email)
            if not bo:
                return Response({"error":"Account does not exist"}, status=status.HTTP_404_NOT_FOUND)
            user = authenticate(email=email, password=password)
            if not user:
                return Response({"error":"Incorrect password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            jwt_token = RefreshToken.for_user(user)
            payload = {}
            payload["message"] = "Login Successfull"
            payload["tid"] = bo.tid
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
            email = serializer.validated_data["email"]
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
            otp = serializer.validated_data["otp"]
            cached_email = cache.get(otp)
            if not cached_email:
                return Response({"error":"OTP expired"}, status=status.HTTP_408_REQUEST_TIMEOUT)
            if not BeatOfficerModel.objects.filter(email=cached_email).first():
                return Response({"error":"User does not Exist"}, status=status.HTTP_404_NOT_FOUND)
            user_obj = BeatOfficerModel.objects.get(email=cached_email)
            user_obj.set_password(serializer.validated_data["password"])
            user_obj.save()
            cache.delete(otp)
            return Response({"message":"Password Changed Successfull"}, status=status.HTTP_202_ACCEPTED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def bo_new(request, joining_code):
    try:
        ser = emailSerializer(data=request.data)
        if ser.is_valid():
            email = ser.validated_data["email"]
            if not BeatOfficerModel.objects.filter(email=email).exists():
                return Response({"error":"Account does not exist"}, status=status.HTTP_404_NOT_FOUND)
            user = authenticate(email=email, password=joining_code)
            if not user:
                return Response({"error":"Incorrect password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            jwt_token = RefreshToken.for_user(user)
            return Response({"message":"Login Successfull, enter personal details", "token":str(jwt_token.access_token)}, status=status.HTTP_202_ACCEPTED)
        return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def bo_personal_details(request):
    try:
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        ser = BOPersonalDetails(data=request.data)
        if ser.is_valid():
            bo.name = ser.validated_data["name"]
            bo.address = ser.validated_data["address"]
            bo.profile_pic = ser.validated_data["profile_pic"]
            bo.set_password(ser.validated_data["password"])
            bo.save()
            return Response({"message": "Profile Updated"}, status=status.HTTP_202_ACCEPTED)
        return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

###################################################################################################################


@api_view(["POST"])
def officer_login(request):
    try:
        data = request.data
        serializer = emailSerializer(data=data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            if not OfficerModel.objects.filter(email=email).exists():
                return Response({"error":"Account does not exist"}, status=status.HTTP_404_NOT_FOUND)
            thread_obj = send_login_otp(email)
            thread_obj.start()
            return Response({"message": "Login OTP Sent"}, status=status.HTTP_202_ACCEPTED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def officer_login_otp(request):
    try:
        data = request.data
        serializer = otpSerializer(data=data)
        if serializer.is_valid():
            password = serializer.validated_data["password"]
            otp = serializer.validated_data["otp"]
            user_email = cache.get(otp)
            if not cache.get(otp):
                return Response({"message":"OTP invalid or expired"}, status=status.HTTP_408_REQUEST_TIMEOUT)
            obj = OfficerModel.objects.filter(email=user_email).first()
            if obj is None:
                return Response({"message":"Account does not exist"}, status=status.HTTP_404_NOT_FOUND)
            user = authenticate(email=user_email, password=password)
            if not user:
                return Response({"message":"Incorrect password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            jwt_token = RefreshToken.for_user(user)
            cache.delete(otp)
            return Response({"message":"Login successfull", "token":str(jwt_token.access_token), "post":obj.post}, status=status.HTTP_202_ACCEPTED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def officer_forgot(request):
    try:
        data = request.data
        serializer = emailSerializer(data=data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
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
            otp = serializer.validated_data["otp"]
            cached_email = cache.get(otp)
            if not cached_email:
                return Response({"error":"OTP expired"}, status=status.HTTP_408_REQUEST_TIMEOUT)
            if not OfficerModel.objects.filter(email=cached_email).first():
                return Response({"error":"User does not Exist"}, status=status.HTTP_404_NOT_FOUND)
            user_obj = OfficerModel.objects.get(email=cached_email)
            user_obj.set_password(serializer.validated_data["password"])
            user_obj.save()
            cache.delete(otp)
            return Response({"message":"Password Changed Successfull"}, status=status.HTTP_202_ACCEPTED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



###################################################################################################################


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def beat_officer_profile(request):
    try:
        bo = BeatOfficerModel.objects.get(email=request.user.email)
        serializer = BeatOfficerProfileSerializer(bo)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
