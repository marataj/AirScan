from django.db import models

# Create your models here.

class DestinationsModel(models.Model):
    class Meta:
        db_table = "destinations_db"

    callsign = models.CharField(max_length=10, primary_key=True)
    origin = models.CharField(max_length=15)
    destination = models.CharField(max_length=15)