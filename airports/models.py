from django.db import models

# Create your models here.

model_key_map = {
    'id': '_id',
    'ident': 'ident',
    'type': 'type',
    'name': 'name',
    'latitude_deg': 'latitude_deg',
    'longitude_deg': 'longitude_deg',
    'elevation_ft': 'elevation_ft',
    'continent': 'continent',
    'iso_country': 'iso_country',
    'iso_region': 'iso_region',
    'municipality': 'municipality',
    'scheduled_service': 'scheduled_service',
    'gps_code': 'gps_code',
    'iata_code': 'iata_code',
    'local_code': 'local_code',
    'home_link': 'home_link',
    'wikipedia_link': 'wikipedia_link',
    'keywords': 'keywords'
    }

class Airports(models.Model):
    """
    Model containing data about airports. Model is corresponding with https://ourairports.com/data/
    
    """
    id = models.AutoField(primary_key=True)
    _id = models.IntegerField()
    ident = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    latitude_deg = models.FloatField()
    longitude_deg = models.FloatField()
    elevation_ft = models.FloatField()
    continent = models.CharField(max_length=50, blank=True)
    iso_country = models.CharField(max_length=50, blank=True)
    iso_region = models.CharField(max_length=50, blank=True)
    municipality = models.CharField(max_length=50, blank=True)
    scheduled_service = models.BooleanField()
    gps_code = models.CharField(max_length=50)
    iata_code = models.CharField(max_length=50, blank=True)
    local_code = models.CharField(max_length=50, blank=True)
    home_link = models.CharField(max_length=200, blank=True)
    wikipedia_link = models.CharField(max_length=200, blank=True)
    keywords = models.CharField(max_length=200, blank=True)
    
    def __str__(self) -> str:
        return self.name + "; " + self.iso_country