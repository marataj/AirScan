from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from airplanes.models import AirplaneModel
from airports.models import AirportsModel
from utils.map_utils import add_airport_marker, generate_generic_map

from .models import FavoritesListModel

# Create your views here.


def favorites_view(request):
    """
    Function representing view with list of favorites items.

    """
    favorites_list = FavoritesListModel.objects.filter(user_name=request.user.username)
    favorites_airports = AirportsModel.objects.filter(
        ident__in=[i.icao24 for i in favorites_list.filter(record_type="airport")]
    )
    favorites_aircrafts = AirplaneModel.objects.filter(
        icao24__in=[i.icao24 for i in favorites_list.filter(record_type="airplane")]
    )

    map, _ = generate_generic_map()
    for airport in favorites_airports:
        map = add_airport_marker(
            map, airport.latitude_deg, airport.longitude_deg, airport, airport.ident
        )
    map.render()
    map_html = map._repr_html_()

    return render(
        request,
        "favorites/favorites.html",
        {
            "airports_list": favorites_airports,
            "aircrafts_list": favorites_aircrafts,
            "html": map_html,
        },
    )


def add(request):
    """
    Endpoint responsible for adding an new item to the favorites list.

    """
    if request.method == "POST":
        favorite = request.POST["icao24"]
        FavoritesListModel(
            user_name=request.user.username,
            icao24=request.POST["icao24"],
            record_type=request.POST["type"],
        ).save()
        messages.success(
            request,
            f"{request.POST['type'].capitalize()} {request.POST['icao24']} added to favorites!",
            extra_tags="success",
        )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"), request.POST)


def delete(request):
    """
    Endpoint responsible for removing the item from the favorites list.

    """
    if request.method == "POST":
        favorite = request.POST["icao24"]
        FavoritesListModel.objects.filter(icao24=request.POST["icao24"]).delete()
        messages.warning(
            request,
            f"{request.POST['icao24']} removed from favorites!",
            extra_tags="warning",
        )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"), request.POST)
