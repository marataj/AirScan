import json
import os

from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from folium import PolyLine
from opensky_api import FlightData, OpenSkyApi

from utils.map_utils import add_airport_marker, bbox_parse, generate_generic_map

from .forms import AirportFlightsForm
from .models import AirportsModel

OPENSKY_USERNAME = os.getenv("OPENSKY_USERNAME")
OPENSKY_PASSWORD = os.getenv("OPENSKY_PASSWORD")


class AirportsView(View):
    """
    Class represents the AirportsView.

    """

    def get(self, request):
        map, _ = generate_generic_map()
        selected_category = "large_airport"
        for airport in AirportsModel.objects.filter(type=selected_category):
            map = add_airport_marker(
                map, airport.latitude_deg, airport.longitude_deg, airport, airport.ident
            )
        map.render()
        map_html = map._repr_html_()

        categories = AirportsModel.objects.values_list("type", flat=True).distinct()
        categories = list(categories)
        categories.append("All")
        print(categories)
        return render(
            request,
            "airports.html",
            {
                "html": map_html,
                "categories": categories,
                "selected_category": selected_category,
            },
        )

    def post(self, request):
        areas = json.loads(request.POST["scanning_area"])
        map_info = json.loads(request.POST["map_info"])
        selected_category = request.POST["category"]

        area_coordinates = bbox_parse(areas)
        map, _ = generate_generic_map(
            map_info["lat"], map_info["lng"], map_info["zoom"]
        )

        filtered_airports = AirportsModel.objects.filter(
            latitude_deg__gte=area_coordinates[0],
            latitude_deg__lte=area_coordinates[1],
            longitude_deg__gte=area_coordinates[2],
            longitude_deg__lte=area_coordinates[3],
        )
        if selected_category != "All":
            filtered_airports = filtered_airports.filter(type=selected_category)

        for airport in filtered_airports:
            map = add_airport_marker(
                map, airport.latitude_deg, airport.longitude_deg, airport, airport.ident
            )

        map.render()
        map_html = map._repr_html_()

        categories = AirportsModel.objects.values_list("type", flat=True).distinct()
        categories = list(categories)
        categories.append("All")
        return render(
            request,
            "airports.html",
            {
                "html": map_html,
                "categories": categories,
                "selected_category": selected_category,
                "airports_list": filtered_airports,
            },
        )


class AirportDetailsView(DetailView):
    """
    Class representing the detail view of Airports Model.

    """

    template_name = "airport_details.html"
    model = AirportsModel

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        map, _ = generate_generic_map(
            self.object.latitude_deg,
            self.object.longitude_deg + 0.1,
            zoom=12,
            draw=False,
        )
        map = add_airport_marker(
            map,
            self.object.latitude_deg,
            self.object.longitude_deg,
            self.object.municipality,
            self.object.ident,
        )
        map.render()
        map_html = map._repr_html_()
        context["raw_map"] = map
        context["html"] = map_html
        context["form"] = AirportFlightsForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = AirportFlightsForm(request.POST)
        context = self.get_context_data()
        if form.is_valid():
            open_sky = OpenSkyApi(OPENSKY_USERNAME, OPENSKY_PASSWORD)
            begin = form.cleaned_data.get("begin_time")
            end = form.cleaned_data.get("end_time")
            data_type = form.cleaned_data.get("type")
            data: list[FlightData] = []
            map = context["raw_map"]
            search_field_name = ""
            if data_type == "1":
                data = open_sky.get_departures_by_airport(
                    airport=self.kwargs["pk"].strip(),
                    begin=int(begin.timestamp()),
                    end=int(end.timestamp()),
                )
                search_field_name = "estArrivalAirport"
            if data_type == "2":
                data = open_sky.get_arrivals_by_airport(
                    airport=self.kwargs["pk"].strip(),
                    begin=int(begin.timestamp()),
                    end=int(end.timestamp()),
                )
                search_field_name = "estDepartureAirport"

            for flight in data:
                airport = AirportsModel.objects.filter(
                    ident=getattr(flight, search_field_name)
                )
                if len(airport) <= 0:
                    continue

                map = add_airport_marker(
                    map,
                    airport[0].latitude_deg,
                    airport[0].longitude_deg,
                    airport[0].municipality,
                    airport[0].ident,
                )
                PolyLine(
                    [
                        (airport[0].latitude_deg, airport[0].longitude_deg),
                        (
                            self.object.latitude_deg,
                            self.object.longitude_deg,
                        ),
                    ],
                    color="red",
                    weight=1,
                    opacity=1,
                ).add_to(map)
                context["flights"] = data
            map.render()
            map_html = map._repr_html_()
            context["html"] = map_html
        context["form"] = form

        return self.render_to_response(context=context)
