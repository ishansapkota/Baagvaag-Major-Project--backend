from django.shortcuts import render
from django.http import JsonResponse
from .models import userRegister
from .serializers import RegistrationsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import jwt,datetime


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
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .utils import send_email_verification,forgot_password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate,login,logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator




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
                if (serializer.errors.get('email')):
                    return Response({"message":"Email is required/already exists"},status=status.HTTP_400_BAD_REQUEST)
                elif(serializer.errors.get('firstName')):
                    return Response({'message':'Error in first name field'},status=status.HTTP_400_BAD_REQUEST)
                elif(serializer.errors.get('lastName')):
                    return Response({'message':'Error in last name field'},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                
            
            #remove password2
            #image url, if not sent image put default image url
            
           
class EmailVerification(APIView):
     def get(self,request,id,token):
        if request.method == "GET":    
            try:
                user = User.objects.get(id=id)
                custom_user = userRegister.objects.get(user_id = id)
            except:
                return Response("User not found", status=status.HTTP_404_NOT_FOUND)
            if default_token_generator.check_token(user,token):
                user.is_active = True
                custom_user.is_verified = True
                user.save()
                custom_user.save()
                return Response("Email has been verified",status=status.HTTP_202_ACCEPTED)
            else:
                return Response("The token is invalid",status=status.HTTP_400_BAD_REQUEST)
        
# @method_decorator(csrf_exempt, name='dispatch')
class handleLogin(APIView):
     def post(self,request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = authenticate(username = request.data['email'],password = request.data['password'])
            #check_user = userRegister.objects.get(email = request.data['email'])
            
            if user == None:
                return Response("User must be verified first!",status=status.HTTP_400_BAD_REQUEST)
            # if user is None: #since if there is no user
            # if check_user.is_verified == None:
            #     return Response("User must be verified first!",status=status.HTTP_400_BAD_REQUEST)
            
            if user:
                login(request,user)
                #return Response("User successfully logged in.",status=status.HTTP_202_ACCEPTED)
                
                refresh = RefreshToken.for_user(user)
                
                if user.is_staff == False and user.is_active==True:
                    # and check_user.is_verified == True
                    return Response({
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'role' : "User"
                        })
                elif user.is_superuser == True and user.is_staff== True:
                    return Response({"message":{
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'role' : "Admin"
                        }})
                
                elif user.is_staff == True:
                    return Response({"message":{
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'role' : "Ranger"
                        }})
                
                else:
                    return Response("Invalid!",status=status.HTTP_401_UNAUTHORIZED)
                # else:
                #     return Response("User must be verified!Check your email for verification mail.",status=status.HTTP_403_FORBIDDEN)
            else:
                return Response("Invalid attempt to log in.",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Invalidated attempt",status=status.HTTP_400_BAD_REQUEST)

class handleLogout(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            logout(request)
            return Response({"message":"User has been logged out."},status=status.HTTP_200_OK)
        else:
            return Response("User is not authenticated.",status=status.HTTP_401_UNAUTHORIZED)
        
class ForgotPassword(APIView):
    def post(self,request):
        serializer = ForgotPasswordSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if email:
                user = User.objects.get(email=email)
                reset_link = forgot_password(user)
                # password = request.data('password')
                # if default_token_generator.check_token(user,token):
                #     user.set_password(password)
                #     user.save()
                return Response({"message": "Check your email for password reset link!", "reset_link": reset_link},status=status.HTTP_201_CREATED)
            else:
                return Response("Email not registered!",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Invalid request.",status=status.HTTP_400_BAD_REQUEST)
        
        #add some sort of verification inorder to know if the user is true
        
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


# class KYCAPI(APIView):
#     def get(self,request,id):
#         try:
#             user = userRegister.objects.filter(user_id=id)
#             serializer = KYCSerializer(user,many=True)
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         except userRegister.DoesNotExist:
#             return Response({"message":"User doesnot exist."},status=status.HTTP_400_BAD_REQUEST)

#     def put(self,request,id):
#         try:
#             user = userRegister.objects.filter(user_id=id)
#             serializer1 = KYCSerializer(user,data=request.data)
#             if serializer1.is_valid():
#                 serializer1.save()
#                 authuser = User.objects.update(first_name = serializer1.validated_data['firstName'],last_name=serializer1.validated_data['lastName'],email=serializer1.validated_data['email'])
#                 authuser.save()

#                 return Response({"message":"Changes made successfully!"},status=status.HTTP_200_OK)
#             return Response({"message":"Invalid Request!"},status=status.HTTP_400_BAD_REQUEST)
#         except userRegister.DoesNotExist:
#             return Response({"message":"User doesnot exist!"},status=status.HTTP_400_BAD_REQUEST)
class KYCAPI(APIView):
    def get(self, request, id):
        try:
            user = userRegister.objects.filter(user_id=id)
            serializer = KYCSerializer(user,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except (User.DoesNotExist, userRegister.DoesNotExist):
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            authuser = User.objects.get(id=id)
            user_profile = userRegister.objects.get(user_id=id)
            serializer = KYCSerializer(user_profile, data=request.data, partial=True)
            if serializer.is_valid():
                authuser.first_name = serializer.validated_data['firstName']
                authuser.last_name = serializer.validated_data['lastName']
                authuser.email = serializer.validated_data['email']
                authuser.save()

                serializer.save()
                # user_profile.firstName = serializer.validated_data['firstName']
                # user_profile.lastName = serializer.validated_data['lastName']
                # user_profile.email = serializer.validated_data['email']
                # user_profile.userImageURL = serializer.validated_data['userImageURL']
                # user_profile.phone = serializer.validated_data['phone']
                # user_profile.save()

                return Response({"message": "Changes made successfully!"}, status=status.HTTP_200_OK)
            return Response({"message": "Invalid Request!"}, status=status.HTTP_400_BAD_REQUEST)
        except userRegister.DoesNotExist:
            return Response({"message": "User does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

class AddRanger(APIView):
    def post(self,request):
        if request.user.is_superuser:
            serializer = RangerAddSerializer(data=request.data)
            if serializer.is_valid():
                
                serializer.save()
                return Response("Ranger has been added to the database.",status=status.HTTP_200_OK)
            else:
                return Response("Not added in the database.",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Only admin can access this.",status=status.HTTP_400_BAD_REQUEST)
        
# class DeleteUser(APIView):
#     def get(self,request):
#         if request.user.is_superuser:

class ListUsers(APIView):
    def get(self,request):
        if request.user.is_superuser:
            user_data = User.objects.filter(is_superuser=False, is_staff=False)
            serializer = ListUsersSerializer(user_data,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response("you must be an admin to call this.",status=status.HTTP_400_BAD_REQUEST)

class ListRangers(APIView):
    def get(self,request):
        if request.user.is_superuser:
            ranger_data = User.objects.filter(is_superuser = False , is_staff = True)
            serializers = ListUsersSerializer(ranger_data, many=True)
            return Response(serializers.data,status=status.HTTP_200_OK)
        
        else:
            return Response("you must be an admin to call this.",status=status.HTTP_400_BAD_REQUEST)
        
class ChangeToAdmin(APIView):
    def get(self,request,id):
        if request.user.is_active:
            user = User.objects.get(id=id)
            user.is_superuser = True
            user.save()
            return Response("User has been set to an Admin",status=status.HTTP_200_OK)

class DeleteUserAdmin(APIView):
    def get(self,request,id):
        if request.user.is_superuser:
            user = User.objects.get(id = id)
            user_register = userRegister.objects.get(user_id= id)
            user_register.delete()
            user.delete()
            return Response("The user has been deleted", status=status.HTTP_200_OK)
        else:
            return Response("Not deleted",status=status.HTTP_400_BAD_REQUEST)
        

class DeleteRangerAdmin(APIView):
    def get(self,request,id):
        if request.user.is_superuser:
            user = User.objects.get(id=id)
            user.delete()
            return Response("The ranger has been deleted",status=status.HTTP_200_OK)
        else:
            return Response("Not Deleted",status=status.HTTP_400_BAD_REQUEST)
            


