from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from pathlib import Path
import folium
from folium.plugins import Draw
# Create your views here.

def HomeView(request):
    return render(request, "home.html")


class Map(View):
    def get(self, request):
        m = folium.Map(location=[41.157944, -8.629105], width='100%', height='100%', zoom_start=12, tiles="OpenStreetMap" )
        Draw(
        export=False,
        filename="my_data.geojson",
        position="topleft",
        draw_options={"polyline": False,
        "polygon": False,
        "circle": False,
        "marker": False,
        "circlemarker": False
        },
        edit_options={"edit": False},
        ).add_to(m)
        m.render()
        html_string = m._repr_html_()
        html_string = html_string.replace("></iframe>", " id='iframik'></iframe>")
        # html_string = m.get_root().render()
        return render(request, "map.html", {"html": html_string,})
         
