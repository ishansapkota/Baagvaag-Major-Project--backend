from rest_framework import serializers
from .models import Victim

class VictimAddSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only= True)
    class Meta:
        model = Victim
        fields = ['id','victimName','victimAge','victimAddress','victimPhoto','victimCertificate']