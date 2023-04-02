from pathlib import Path
from typing import Optional, Tuple

import folium
from folium.features import CustomIcon
from folium.plugins import Draw

from AirScan.settings import BASE_DIR


def validate_latitude(lat: float) -> float:
    min = -90
    max = 90
    range = max - min
    if lat > min and lat < max:
        return lat
    if lat < min:
        return range - lat
    if lat > max:
        return lat - range


def validate_longitude(lng: float) -> float:
    min = -180
    max = 180
    range = max - min
    if lng > min and lng < max:
        return lng
    if lng < min:
        return range - lng
    if lng > max:
        return lng - range


def bbox_parse(area_list: list) -> list:
    min_lat: float = 90.0
    max_lat = -90
    min_lng = 180
    max_lng = -180

    for area in area_list:
        min_lat = (
            float(area["SW"]["lat"]) if float(area["SW"]["lat"]) < min_lat else min_lat
        )
        min_lng = (
            float(area["SW"]["lng"]) if float(area["SW"]["lng"]) < min_lng else min_lng
        )
        max_lat = area["NE"]["lat"] if area["NE"]["lat"] > max_lat else max_lat
        max_lng = area["NE"]["lng"] if area["NE"]["lng"] > max_lng else max_lng

    return [
        validate_latitude(min_lat),
        validate_latitude(max_lat),
        validate_longitude(min_lng),
        validate_longitude(max_lng),
    ]


def generate_generic_map(
    center_lat: Optional[float] = 52.40,
    center_lon: Optional[float] = 16.93,
    zoom: Optional[int] = 8,
) -> Tuple[folium.Map, str]:
    m = folium.Map(
        location=[validate_latitude(center_lat), validate_longitude(center_lon)],
        width="100%",
        height="100%",
        zoom_start=zoom,
        tiles="OpenStreetMap",
    )
    Draw(
        export=False,
        filename="my_data.geojson",
        position="topleft",
        draw_options={
            "polyline": False,
            "polygon": False,
            "circle": False,
            "marker": False,
            "circlemarker": False,
        },
        edit_options={"edit": False},
    ).add_to(m)
    m.render()
    html_string = m._repr_html_()  # FIXME: remove?
    return m, html_string


def add_plane_marker(
    map: folium.Map, lat: float, lng: float, popup_msg: str
) -> folium.Map:
    folium.Marker(
        location=[
            validate_latitude(lat),
            validate_longitude(lng),
        ],
        popup=popup_msg,
        icon=CustomIcon(
            icon_image=str(Path(BASE_DIR, "static/images/plane.png")),
            icon_size=(30, 30),
        ),
    ).add_to(map)
    return map


def add_airport_marker(
    map: folium.Map, lat: float, lng: float, popup_msg: str
) -> folium.Map:
    folium.Marker(
        location=[
            validate_latitude(lat),
            validate_longitude(lng),
        ],
        popup=popup_msg,
    ).add_to(map)
    return map
