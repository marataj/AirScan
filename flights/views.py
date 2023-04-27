from django.shortcuts import render
from django.views import View

from airplanes.models import AirplaneModel
from utils.general_tools import json_to_dict_parse
from utils.map_utils import add_plane_marker, generate_generic_map
from utils.planespotters_api import get_airplane_photo_url
from utils.state_vector_extended import StateVectorExtended


# Create your views here.
class FlightView(View):
    """
    Class representing the view displaying single flight information.

    """

    def get(self, request, **kwargs):
        flight = StateVectorExtended(
            StateVectorExtended.prepare_input_list(json_to_dict_parse(kwargs["flight"]))
        )
        map, _ = generate_generic_map(
            flight.latitude, flight.longitude, zoom=12, draw=False
        )
        map = add_plane_marker(
            map, flight.latitude, flight.longitude, flight.true_track, flight.icao24
        )
        map.render()
        map_html = map._repr_html_()

        airplane_url = get_airplane_photo_url(flight.icao24)
        airplane_info = AirplaneModel.objects.filter(icao24=flight.icao24)
        return render(
            request,
            "flight_overview.html",
            {
                "html": map_html,
                "flight": flight,
                "photo": airplane_url,
                "airplane_details": airplane_info[0] if len(airplane_info) else None,
            },
        )
