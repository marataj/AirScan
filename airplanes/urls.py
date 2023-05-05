from django.urls import path
from .views import AircraftDetailView, AircraftFormView

urlpatterns = [
    path("", AircraftFormView.as_view(), name="aircraft_form"),
    path("<str:pk>", AircraftDetailView.as_view(), name="aircraft_details"),
]