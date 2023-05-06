from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views import View

# Create your views here.


class UserCreationView(View):
    """
    Class representing user registration view.

    """
    def get(self, request):
        return render(
            request, "user/create_user.html", {"user_creation_form": UserCreationForm()}
        )

    def post(self, request):
        user_creation_form = UserCreationForm(request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            return redirect("home_page")
        return render(
            request, "user/create_user.html", {"user_creation_form": user_creation_form}
        )


class UserLoginView(LoginView):
    """
    Class representing login view.

    """
    template_name = "user/login.html"
    next_page = "home_page"


def logout_view(request):
    logout(request)
    return redirect("home_page")
