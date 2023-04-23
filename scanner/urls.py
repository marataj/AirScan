from django.urls import path
from .views import Scanner, Flight

urlpatterns = [
    path("", Scanner.as_view(), name="scanning_page"),
    path("flight/<flight>", Flight.as_view(), name="flight"),
]