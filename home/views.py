from django.shortcuts import render

# Create your views here.

def HomeView(request):
    """
    Function representing home page view.

    """
    return render(request, "home.html")