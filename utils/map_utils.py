from pathlib import Path
from typing import Optional, Tuple

import folium
from folium import plugins


def validate_latitude(lat: float) -> float:
    """
    Utility function responsible for validating of the latitude. Prevents multiplying of the validated
    points among expandable map.

    Parameters
    ----------
    lat : float
        Latitude of the validated point.

    Returns
    -------
    float
        Corrected latitude.

    """
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
    """
    Utility function responsible for validating of the longitude. Prevents multiplying of the validated
    points among expandable map.

    Parameters
    ----------
    lng : float
        Longitude of the validated point.

    Returns
    -------
    float
        Corrected longitude.

    """
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
    """
    Utility function that parses coordinates of the multiple areas to one general area that contains all areas from the list.

    Parameters
    ----------
    area_list : list
        List of the areas

    Returns
    -------
    list
        Coordinates of one general area containing all the areas from the list.

    """
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
    draw: Optional[bool] = True,
) -> Tuple[folium.Map, str]:
    """
    Utility function generating generic foolium map.

    Parameters
    ----------
    center_lat : Optional[float], optional
        Latitude of the center point of the map, by default 52.40.
    center_lon : Optional[float], optional
        Longitude of the center point of the map, by default 16.93.
    zoom : Optional[int], optional
        Starting zoom factor, by default 8.
    draw : Optional[bool], optional
        Boolean flag indicates if drawing section will be generated, by default True.

    Returns
    -------
    Tuple[folium.Map, str]
        folium.Map
            generated map.
        str
            rendered html with embedded map.
    """
    m = folium.Map(
        location=[validate_latitude(center_lat), validate_longitude(center_lon)],
        width="100%",
        height="100%",
        zoom_start=zoom,
        tiles="OpenStreetMap",
    )
    if draw:
        plugins.Draw(
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
    html_string = m._repr_html_()
    return m, html_string


def add_plane_marker(
    map: folium.Map, lat: float, lng: float, angle: float, popup_msg: str
) -> folium.Map:
    """
    Utility function that adds the markers of the plane to the passed folium map.

    Parameters
    ----------
    map : folium.Map
        The map that will be decorated by new marker.
    lat : float
        Latitude of new marker.
    lng : float
        Longitude of new marker.
    angle : float
        Marker rotation angle.
    popup_msg : str
        Message to show in marker hint.

    Returns
    -------
    folium.Map
        Map with new marker added.

    """
    folium.Marker(
        location=[
            validate_latitude(lat),
            validate_longitude(lng),
        ],
        popup=popup_msg,
        icon=plugins.BeautifyIcon(
            icon="plane",
            border_color="transparent",
            background_color="transparent",
            border_width=1,
            text_color="#003EFF",
            inner_icon_style="margin:0px;font-size:2em;transform: rotate({0}deg);".format(
                angle - 90
            ),
        ),
    ).add_to(map)
    return map


def add_airport_marker(
    map: folium.Map, lat: float, lng: float, popup_msg: str, ident: str
) -> folium.Map:
    """
    Utility function that adds the markers of the airport to the passed folium map.


    Parameters
    ----------
    map : folium.Map
        The map that will be decorated by new marker.
    lat : float
        Latitude of new marker.
    lng : float
        Longitude of new marker.
    popup_msg : str
        Message to show in marker hint.

    Returns
    -------
    folium.Map
        Map with new marker added.
    """
    popup = f"""
    <a href="/airports/airport/{ident}" target="_blank">
        {popup_msg}
    </a>
    """
    folium.Marker(
        location=[
            validate_latitude(lat),
            validate_longitude(lng),
        ],
        popup=popup,
    ).add_to(map)
    return map
