from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import VictimAddSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Victim
# Create your views here.

class AddVictim(APIView):
    def post(self,request):
        try:
            if request.user.is_superuser:
                serializer = VictimAddSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response("The victim has been added.",status=status.HTTP_200_OK)
                else:
                    return Response("Invalid Attempt",status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Must have admin perms",status=status.HTTP_400_BAD_REQUEST)
            
        except:
            return Response("Exception.",status=status.HTTP_400_BAD_REQUEST)
        
class ViewVictim(APIView):
    def get(self,request):
        try:
            victim = Victim.objects.all()
            serializer = VictimAddSerializer(victim,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response("Exception.",status=status.HTTP_400_BAD_REQUEST)
        
class EditVictimInfo(APIView):
    def put(self,request,id):
        try:
            if request.user.is_superuser:    
                victim = Victim.objects.get(id=id)
                serializer = VictimAddSerializer(victim,data=request.data)
                if serializer.is_valid():
                    # victim.victimName = serializer.validated_data['victimName']
                    # victim.victimAddress = serializer.validated_data['victimAddress']
                    # victim.victimAge = serializer.validated_data['victimAge']
                    # victim.victimPhoto = serializer.validated_data['victimPhoto']
                    # victim.victimCertificate = serializer.validated_data['victimCertificate']
                    serializer.save()
                    return Response("The victim's info has been updated",status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("Invalid Attempt",status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Must have admin perms",status=status.HTTP_400_BAD_REQUEST)
                
        except:
            return Response("Exception",status=status.HTTP_400_BAD_REQUEST)
        
class DeleteVictimInfo(APIView):
    def delete(self,request,id):
        try:
            if request.user.is_superuser:    
                victim = Victim.objects.get(id=id)
                victim.delete()
                return Response("The victim's info has been deleted!",status=status.HTTP_200_OK)
            else:
                return Response("Must have admin perms",status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Exception",status=status.HTTP_400_BAD_REQUEST)
                
