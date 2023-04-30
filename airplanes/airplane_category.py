airplane_categories={
    -1: "All",
    0 : "No info", 
    1 : "No Category Info",
    2 : "Light", 
    3 : "Small", 
    4 : "Large", 
    5 : "High Vortex Large",
    6 : "Heavy",
    7 : "High Performance",
    8 : "Rotorcraft",
    9 : "Glider / sailplane",
    10 : "Lighter-than-air",
    11 : "Parachutist",
    12 : "Ultralight",
    13 : "Reserved",
    14 : "Unmanned",
    15 : "Trans-atmospheric" ,
    16 : "Emergency Vehicle",
    17 : "Service Vehicle",
    18 : "Point Obstacle",
    19 : "Cluster Obstacle",
    20 : "Line Obstacle"
    }

def get_airplane_category(idx: int) -> str:
    """
    Get the airplane category defined by the OpenSkyApi

    Parameters
    ----------
    idx : int
        Index of category

    Returns
    -------
    str
        Airplane category name

    """
    return airplane_categories.get(idx, "No info")