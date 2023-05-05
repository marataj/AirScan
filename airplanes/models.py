from typing import List
from django.urls import reverse

from django.db import models

# Create your models here.


class AirplaneModel(models.Model):
    """
    Model stores information about airplanes. Based on csv database from OpenSkyNetwork.
    https://opensky-network.org/aircraft-database

    """

    # TODO replace hardcoding with global parameters
    class Meta:
        db_table = "airplanes_db"

    icao24 = models.CharField(max_length=10, primary_key=True)
    registration = models.CharField(max_length=20)
    manufacturername = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serialnumber = models.CharField(max_length=50)
    operator = models.CharField(max_length=50)
    owner = models.CharField(max_length=50)
    categoryDescription = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"Model:{self.manufacturername}: {self.model}. Owner: {self.owner}"

    def get_absolute_url(self):
        return reverse("aircraft_details", kwargs={"pk": self.icao24})
    

    @classmethod
    def get_fields_names(cls) -> List[str]:
        return [field.name for field in cls._meta.fields]
