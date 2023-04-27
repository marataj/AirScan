from django.urls import path
from .views import FlightView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("overview/<flight>", FlightView.as_view(), name="flight_overview"),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)