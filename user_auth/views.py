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
from .serializers import RegistrationsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .utils import send_email_verification
from django.contrib.auth.models import User


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
                # email = serializer.validated_data.get('email')
                # print(email)
                
                # user = User.objects.filter(email=email).first()
                # print(user)
                data = serializer.validated_data
                print(data)
                user = serializer.create(data)
                print(user)
                if user:
                    result = send_email_verification(user)
                    if result:   
                            serializer.save()
                            return Response("Verification link has been sent to your email.",status=status.HTTP_201_CREATED)
                            
                    else:
                            return Response("Verification has not been sent.",status=status.HTTP_400_BAD_REQUEST)
                else:  
                    return Response("User not found.", status=status.HTTP_404_NOT_FOUND)
                    # return Response("User verification")
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
