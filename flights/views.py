from django.shortcuts import render
from django.views import View
from folium import PolyLine

from airplanes.models import AirplaneModel
from airports.models import AirportsModel
from favorites.models import FavoritesListModel
from utils.general_tools import json_to_dict_parse
from utils.map_utils import add_airport_marker, add_plane_marker, generate_generic_map
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

        airplane_details = AirplaneModel.objects.filter(icao24=flight.icao24)
        if flight.origin and flight.destination:
            origin_airport = AirportsModel.objects.filter(ident=flight.origin.strip())[
                0
            ]
            destination_airport = AirportsModel.objects.filter(
                ident=flight.destination.strip()
            )[0]
            map = add_airport_marker(
                map,
                origin_airport.latitude_deg,
                origin_airport.longitude_deg,
                origin_airport.municipality,
                origin_airport.ident,
            )
            map = add_airport_marker(
                map,
                destination_airport.latitude_deg,
                destination_airport.longitude_deg,
                destination_airport.municipality,
                destination_airport.ident,
            )
            PolyLine(
                [
                    (origin_airport.latitude_deg, origin_airport.longitude_deg),
                    (flight.latitude, flight.longitude),
                    (
                        destination_airport.latitude_deg,
                        destination_airport.longitude_deg,
                    ),
                ],
                color="red",
                weight=2.5,
                opacity=1,
            ).add_to(map)
        else:
            origin_airport = None
            destination_airport = None

        map.render()
        map_html = map._repr_html_()

        return render(
            request,
            "flight_overview.html",
            {
                "html": map_html,
                "flight": flight,
                "photo": get_airplane_photo_url(flight.icao24),
                "airplane_details": airplane_details[0]
                if len(airplane_details)
                else None,
                "origin_airport": origin_airport,
                "destination_airport": destination_airport,
                "favorite": len(
                    FavoritesListModel.objects.filter(
                        user_name=request.user.username, icao24=flight.icao24
                    )
                )
                == 1,
            },
        )
