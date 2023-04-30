import json
import os

from django.shortcuts import render
from django.views import View
from opensky_api import OpenSkyApi

from flights.models import DestinationsModel
from utils.map_utils import add_plane_marker, bbox_parse, generate_generic_map
from airplanes.airplane_category import airplane_categories

# Create your views here.


OPENSKY_USERNAME = os.getenv("OPENSKY_USERNAME")
OPENSKY_PASSWORD = os.getenv("OPENSKY_PASSWORD")


class ScannerView(View):
    """
    Class represents the scanning page.

    """

    def get(self, request):
        _, map_html = generate_generic_map()
        return render(
            request,
            "scanner.html",
            {"html": map_html,
             "categories": airplane_categories},
        )

    def post(self, request):
        open_sky = OpenSkyApi(OPENSKY_USERNAME, OPENSKY_PASSWORD)
        areas = json.loads(request.POST["scanning_area"])
        map_info = json.loads(request.POST["map_info"])
        selected_category = int(request.POST["category"])
        print(f"CATEGORY -------> {selected_category}")
        flights = open_sky.get_states(bbox=bbox_parse(areas))
        map, _ = generate_generic_map(
            map_info["lat"], map_info["lng"], map_info["zoom"]
        )
        filtered_flights=[]
        for flight in flights.states:
            if flight.category != selected_category and selected_category != -1:
                continue
            dest = DestinationsModel.objects.filter(
                callsign=str(flight.callsign.strip())
            )
            flight.origin = dest[0].origin if len(dest) != 0 else None
            flight.destination = dest[0].destination if len(dest) != 0 else None
            map = add_plane_marker(
                map, flight.latitude, flight.longitude, flight.true_track, flight.icao24
            )
            filtered_flights.append(flight)
        

        map.render()
        map_html = map._repr_html_()

        return render(
            request,
            "scanner.html",
            {"html": map_html, "categories": airplane_categories, "selected_category": selected_category,"flights_list": filtered_flights},
        )
