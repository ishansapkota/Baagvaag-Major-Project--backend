from django.shortcuts import render
from rest_framework.views import APIView
from .utils import KhaltiInitiate,KhaltiVerify
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from .models import VictimDonation
from charity.models import Victim
# Create your views here.

class KhaltiInitiation(APIView):
    def post(self,request,id):
        serializer = AmountSerializer(data= request.data)
        if serializer.is_valid():
        # amount_paisa = request.post('amount')
        # amount  = float(amount_paisa)*100
            amount_paisa = serializer.validated_data['amount']
            amount = float(amount_paisa) * 100
            response_data = KhaltiInitiate(amount)
            if "error" not in response_data:
                victim_id = Victim.objects.get(id=id)
                data = VictimDonation.objects.create(victim = victim_id,amount = amount/100)
                data.save()
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class KhaltiVerification(APIView):
    def post(self,request):
        pidx = request.data['pidx']
        response_data = KhaltiVerify(pidx)
        print(response_data)
        if "error" in response_data:
            return Response(response_data,status=status.HTTP_400_BAD_REQUEST)

        if response_data['status']=="Completed":
            return Response("Done",status=status.HTTP_200_OK)
        else:
            return Response("Not Done",status=status.HTTP_200_OK)