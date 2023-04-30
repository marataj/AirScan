import json

from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from utils.map_utils import add_airport_marker, bbox_parse, generate_generic_map

from .models import AirportsModel


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
    template_name = "airport_details.html"
    model = AirportsModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        map, _ = generate_generic_map(
            self.object.latitude_deg, self.object.longitude_deg, zoom=12, draw=False
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
        context["html"] = map_html
        return context
