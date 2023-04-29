from django.urls import path
from .views import AirportsView, AirportDetailsView

urlpatterns = [
    path("", AirportsView.as_view(), name="airports_map"),
    path("airport/<str:pk>", AirportDetailsView.as_view(), name="airport_details"),
]