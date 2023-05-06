import os

from django.db import models

# Create your models here.


class FavoritesListModel(models.Model):
    """
    Model containing items added to favorites list by users.

    """

    class Meta:
        db_table = str(os.getenv("FAVORITESMODEL_TABLE_NAME"))

    icao24 = models.CharField(max_length=10, primary_key=True)
    record_type = models.CharField(max_length=20)
    user_name = models.CharField(max_length=50)
