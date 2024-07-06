from django.db import models
from charity.models import Victim

# Create your models here.

class VictimDonation(models.Model):
    victim = models.ForeignKey(Victim,on_delete=models.CASCADE,null=True)
    amount = models.FloatField(null=True)