from django.db import models

# Create your models here.
class Stations(models.Model):
    station = models.CharField(max_length=15)