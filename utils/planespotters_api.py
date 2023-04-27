import requests
import json

def get_airplane_photo_url(icao24: str) -> str:
    """
    Utility function that retrieves the photography of particular aircraft, from the https://www.planespotters.net/ API.

    Parameters
    ----------
    icao24 : str
        Registration number of given plane.

    Raises
    ------
    ValueError
        Raises when given airplane was not found in the API DB.

    Returns
    -------
    str
        Link to the aircraft photography.

    """
    url = f"https://api.planespotters.net/pub/photos/hex/{icao24}"
    response = requests.request("GET", url)
    try:
        return response.json()["photos"][0]["thumbnail_large"]["src"]
    except (KeyError, IndexError):
        return None