from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from utils.map_utils import add_airport_marker, generate_generic_map

from .models import AirportsModel


class AirportsView(View):
    """
    Class represents the AirportsView.

    """

    def get(self, request):
        map, _ = generate_generic_map(draw=False)
        for airport in AirportsModel.objects.filter(type="large_airport"):
            map = add_airport_marker(
                map, airport.latitude_deg, airport.longitude_deg, airport, airport.ident
            )
        map.render()
        map_html = map._repr_html_()
        return render(
            request,
            "airports.html",
            {"html": map_html},
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
