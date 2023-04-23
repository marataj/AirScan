from django.shortcuts import render
from django.views import View

from utils.map_utils import add_airport_marker, generate_generic_map

from .models import AirportsModel

# Create your views here.


class AirportsView(View):
    def get(self, request):
        map, _ = generate_generic_map()
        airports = AirportsModel.objects.all()
        for airport in airports:
            map = add_airport_marker(
                map, airport.latitude_deg, airport.longitude_deg, airport
            )
        map.render()
        map_html = map._repr_html_()
        return render(
            request,
            "airports.html",
            {"html": map_html},
        )
