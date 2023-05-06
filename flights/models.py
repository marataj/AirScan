import os

from django.db import models

# Create your models here.


class DestinationsModel(models.Model):
    """
    Class representing model contains data about flights destinations.

    """
    class Meta:
        db_table = str(os.getenv("DESTINATIONSMODEL_TABLE_NAME"))

    callsign = models.CharField(max_length=10, primary_key=True)
    origin = models.CharField(max_length=15)
    destination = models.CharField(max_length=15)
