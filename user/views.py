from django.contrib import messages
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
            messages.success(request, "New user created!", extra_tags="success")
            return redirect("home_page")
        messages.warning(request, "Error. Please retry.", extra_tags="warning")
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
    messages.success(request, "Logged out!", extra_tags="success")
    return redirect("home_page")
