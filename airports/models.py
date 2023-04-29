from django.db import models
from django.urls import reverse

# Create your models here.


class AirportsModel(models.Model):
    """
    Model containing data about airports. Model is corresponding with https://ourairports.com/data/

    """

    # TODO replace hardcoding with parameters
    class Meta:
        db_table = "airports_db"

    ident = models.CharField(max_length=50, primary_key=True)
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    latitude_deg = models.FloatField()
    longitude_deg = models.FloatField()
    elevation_ft = models.FloatField()
    continent = models.CharField(max_length=50, blank=True)
    iso_country = models.CharField(max_length=50, blank=True)
    iso_region = models.CharField(max_length=50, blank=True)
    municipality = models.CharField(max_length=50, blank=True)
    gps_code = models.CharField(max_length=50)
    iata_code = models.CharField(max_length=50, blank=True)
    local_code = models.CharField(max_length=50, blank=True)
    home_link = models.CharField(max_length=200, blank=True)
    wikipedia_link = models.CharField(max_length=200, blank=True)
    keywords = models.CharField(max_length=200, blank=True)

    def __str__(self) -> str:
        return str(self.name) + "; " + str(self.iso_country)

    def get_absolute_url(self):
        return reverse("airport_details", kwargs={"pk": self.pk})
