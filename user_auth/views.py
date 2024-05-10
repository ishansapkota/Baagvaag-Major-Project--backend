from django.shortcuts import render
from django.http import JsonResponse
from .models import userRegister
from .serializers import RegistrationsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView


# Create your views here.
# @api_view(['GET','POST']) #this decorator states the functionality of the function
# def Registration(request):
    

# class Registration(APIView):
#     def post(request):
#         if request.method == 'GET':
#             registered = userRegister.objects.all()
#             serializer = RegistrationsSerializer(registered,many=True)
#             return Response(serializer.data)
    
#     def get(request):
#         if request.method == 'POST':
#             serializer =  RegistrationsSerializer(data = request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data,status=status.HTTP_201_CREATED)

# @api_view(['GET','POST'])

# def Registration(request):
#     if request.method == 'GET':
#         registered = userRegister.objects.all()
#         serializer = RegistrationsSerializer(registered,many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer =  RegistrationsSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response("User created successfully",status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import render
from django.http import JsonResponse
from .models import userRegister
from .serializers import RegistrationsSerializer,LoginSerializer,ForgotPasswordSerializer,ResetPasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .utils import send_email_verification,forgot_password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate,login,logout
from rest_framework_simplejwt.tokens import RefreshToken



# Create your views here.
# @api_view(['GET','POST']) #this decorator states the functionality of the function
# def Registration(request):
    

class Registration(APIView):
    def get(self,request):
        if request.method == 'GET':
            registered = userRegister.objects.all()
            serializer = RegistrationsSerializer(registered,many=True)
            return Response(serializer.data)
    
    def post(self,request):
        if request.method == 'POST':
            serializer =  RegistrationsSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                email = serializer.validated_data.get('email')
                user = User.objects.filter(email=email).first()
                print(user)
                if user:
                    result = send_email_verification(user)
                    if result:   
                            # serializer.save()
                            return Response("Verification link has been sent to your email.",status=status.HTTP_201_CREATED)
                            
                    else:
                            return Response("Verification has not been sent.",status=status.HTTP_400_BAD_REQUEST)
                else:  
                    return Response("User not found.", status=status.HTTP_404_NOT_FOUND)
                    # return Response("User verification")
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
           
class EmailVerification(APIView):
     def get(self,request,id,token):
        if request.method == "GET":    
            try:
                user = User.objects.get(id=id)
            except:
                return Response("User not found", status=status.HTTP_404_NOT_FOUND)
            if default_token_generator.check_token(user,token):
                user.is_active = True
                user.save()
                return Response("Email has been verified",status=status.HTTP_202_ACCEPTED)
            else:
                return Response("The token is invalid",status=status.HTTP_400_BAD_REQUEST)
        

class handleLogin(APIView):
     def post(self,request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = authenticate(username = request.data['email'],password = request.data['password'])
            check_user = User.objects.get(email = request.data['email'])
            
            if check_user.is_active is False:
                return Response("User must be verified first!",status=status.HTTP_400_BAD_REQUEST)
            if user:
                login(request,user)
                #return Response("User successfully logged in.",status=status.HTTP_202_ACCEPTED)
                refresh = RefreshToken.for_user(user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response("Invalid attempt to log in.",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Invalidated attempt",status=status.HTTP_400_BAD_REQUEST)
        

class handleLogout(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            logout(request)
            return Response("User has been logged out.",status=status.HTTP_200_OK)
        else:
            return Response("User is not authenticated.",status=status.HTTP_401_UNAUTHORIZED)
        
class ForgotPassword(APIView):
    def post(self,request):
        serializer = ForgotPasswordSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if email:
                user = User.objects.get(email=email)
                forgot_password(user)
                # password = request.data('password')
                # if default_token_generator.check_token(user,token):
                #     user.set_password(password)
                #     user.save()
                return Response("Check your email for password reset link!",status=status.HTTP_201_CREATED)
            else:
                return Response("Email not registered!",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Invalid request.",status=status.HTTP_400_BAD_REQUEST)
        
class ResetPassword(APIView):
    def post(self,request,id,token):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            confirm_new_password = serializer.validated_data['confirm_new_password']
            if new_password == confirm_new_password:
                user = User.objects.get(id = id)
                password = serializer.validated_data['new_password']
                if default_token_generator.check_token(user,token):
                    user.set_password(password)
                    user.save()
                    return Response("Password resetted successfully!",status=status.HTTP_201_CREATED)
                else:
                    return Response("Invalid Token!",status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Passwords do not match!",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Invalid Request",status=status.HTTP_400_BAD_REQUEST)
