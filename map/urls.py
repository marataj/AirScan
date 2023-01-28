from django.urls import path
from .views import Map, HomeView

urlpatterns = [
    path("map", Map.as_view()),
    path("", HomeView)
]