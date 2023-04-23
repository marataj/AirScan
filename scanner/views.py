import json
import os

from django.shortcuts import render
from django.views import View
from opensky_api import OpenSkyApi

from utils.map_utils import (
    add_plane_marker,
    bbox_parse,
    generate_generic_map,
    validate_latitude,
    validate_longitude,
)

# Create your views here.


OPENSKY_USERNAME = os.getenv("OPENSKY_USERNAME")
OPENSKY_PASSWORD = os.getenv("OPENSKY_PASSWORD")


class Scanner(View):
    def get(self, request):
        _, map_html = generate_generic_map()
        return render(
            request,
            "scanner.html",
            {"html": map_html},
        )

    def post(self, request):
        open_sky = OpenSkyApi(OPENSKY_USERNAME, OPENSKY_PASSWORD)
        areas = json.loads(request.POST["scanning_area"])
        map_info = json.loads(request.POST["map_info"])
        flights = open_sky.get_states(bbox=bbox_parse(areas))
        map, _ = generate_generic_map(
            map_info["lat"], map_info["lng"], map_info["zoom"]
        )

        for flight in flights.states:
            map = add_plane_marker(
                map, flight.latitude, flight.longitude, flight.true_track, flight.icao24
            )

        map.render()
        map_html = map._repr_html_()

        return render(
            request,
            "scanner.html",
            {"html": map_html, "flights_list": flights.states},
        )
