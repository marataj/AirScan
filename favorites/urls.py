from django.urls import path
from .views import favorites_view, add, delete

urlpatterns = [
    path("", favorites_view, name="favorites"),
    path("add", add, name="add_to_favorites"),
    path("delete", delete, name="delete_from_favorites"),
]