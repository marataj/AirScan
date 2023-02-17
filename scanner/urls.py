from django.urls import path
from .views import Scanner

urlpatterns = [
    path("", Scanner.as_view(), name="scanning_page"),
]