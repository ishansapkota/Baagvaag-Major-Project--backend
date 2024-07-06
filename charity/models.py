from django.db import models

# Create your models here.

class Victim(models.Model):
    victimName = models.CharField(max_length=55)
    victimAge = models.CharField(max_length=2)
    victimAddress = models.CharField(max_length=55)
    victimPhoto = models.CharField(null=True)
    victimCertificate = models.CharField(null=True)