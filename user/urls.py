from django.urls import path
from .views import UserCreationView, UserLoginView, logout_view

urlpatterns = [
    path("create", UserCreationView.as_view(), name="user_creation"),
    path("login", UserLoginView.as_view(), name="login"),
    path("logout", logout_view, name="logout"),
]