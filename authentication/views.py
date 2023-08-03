from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate,login
from .decorators import allowed_users
from .serializers import *
from .threads import *
from .models import *
from django.views.decorators.csrf import csrf_exempt


@allowed_users(allowed_roles=['SP'])
@api_view(["POST"])
def signUp(request):
    try:
        data = request.data
        serializer = signupSerializer(data=data)
        if serializer.is_valid():
            name = serializer.data["name"]
            email = serializer.data["email"]
            phone = serializer.data["phone"]
            service_number = serializer.data["service_number"]
            post = serializer.data["post"]
            password = serializer.data["password"]
            
            if SellerModel.objects.filter(email=email).first():
                return Response({"message":"Acount already exists."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            new_customer = SellerModel.objects.create(
                email = email,
                name = name,
                phone = phone,
                post = post,
                service_number = service_number,
                #auth_provider = "email"
            )
            new_customer.set_password(password)
            new_customer.save()
            return Response({"message":"Account created"}, status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(["POST"])
def logIn(request):
    try:
        data = request.data
        serializer = loginSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data["email"]
            password = serializer.data["password"]
            print(password)
            print(email)
            customer_obj = SellerModel.objects.filter(email=email).first()
            if customer_obj is None:
                return Response({"message":"Account does not exist"}, status=status.HTTP_404_NOT_FOUND)
            user = authenticate(email=email, password=password)
            if not user:
                return Response({"message":"Incorrect password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            login(request, user)
            #jwt_token = RefreshToken.for_user(user)
            #return Response({"message":"Login successfull", "token":str(jwt_token.access_token)}, status=status.HTTP_202_ACCEPTED)
            return Response({"message":"Login successfull"}, status=status.HTTP_202_ACCEPTED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(["POST"])
# def forgot(request):
#     try:
#         data = request.data
#         serializer = emailSerializer(data=data)
#         if serializer.is_valid():
#             email = serializer.data["email"]
#             user_obj = CustomerModel.objects.filter(email=email).first()
#             if not user_obj:
#                 return Response({"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
#             if user_obj.auth_provider != "email":
#                 return Response({"message": "Login using Google Auth"}, status=status.HTTP_401_UNAUTHORIZED)
#             thread_obj = send_forgot_link(email)
#             thread_obj.start()
#             return Response({"message":"reset mail sent"}, status=status.HTTP_200_OK)
#         return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(["POST"])
# def reset(request):
#     try:
#         data = request.data
#         serializer = otpSerializer(data=data)
#         if serializer.is_valid():
#             otp = serializer.data["otp"]
#             if not cache.get(otp):
#                 return Response({"message":"OTP expired"}, status=status.HTTP_408_REQUEST_TIMEOUT)
#             if not CustomerModel.objects.filter(email=cache.get(otp)).first():
#                 return Response({"message":"user does not exist"}, status=status.HTTP_404_NOT_FOUND)
#             user_obj = CustomerModel.objects.get(email=cache.get(otp))
#             user_obj.set_password(serializer.data["pw"])
#             user_obj.save()
#             cache.delete(otp)
#             return Response({"message":"Password changed successfull"}, status=status.HTTP_202_ACCEPTED)
#         return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# from django.contrib.auth import authenticate, login
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# def api_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)

#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return JsonResponse({'status': 'success', 'message': 'Login successful.'})
#             else:
#                 return JsonResponse({'status': 'error', 'message': 'User account is not active.'})
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Invalid username or password.'})

#     return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed.'})

