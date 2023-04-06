from django.db import models
from typing import List

# Create your models here.

class AirplaneModel(models.Model):
    """
    Model stores information about airplanes. Based on csv database from OpenSkyNetwork.
    https://opensky-network.org/aircraft-database

    """
    icao24=models.CharField(max_length=10)
    registration=models.CharField(max_length=20)
    manufacturername=models.CharField(max_length=50)
    model=models.CharField(max_length=50)
    serialnumber=models.CharField(max_length=50)
    operator=models.CharField(max_length=50)
    owner=models.CharField(max_length=50)
    categoryDescription=models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"Model:{self.manufacturername}: {self.model}. Owner: {self.owner}"
    
    @classmethod
    def get_fields_names(cls) -> List[str]:
        return [field.name for field in cls._meta.fields]