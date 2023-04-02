from django.urls import path
from .views import AirportsView

urlpatterns = [
    path("", AirportsView.as_view(), name="airports_map"),
]