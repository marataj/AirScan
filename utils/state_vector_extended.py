from opensky_api import StateVector
class StateVectorExtended(StateVector):
    """
    StateVector extended by origin and destination fields.

    """
    keys = [
        "icao24",
        "callsign",
        "origin_country",
        "time_position",
        "last_contact",
        "longitude",
        "latitude",
        "baro_altitude",
        "on_ground",
        "velocity",
        "true_track",
        "vertical_rate",
        "sensors",
        "geo_altitude",
        "squawk",
        "spi",
        "position_source",
        "category",
        "origin",
        "destination"
    ]

    
    def __init__(self, arr):
        self.__dict__ = dict(zip(StateVectorExtended.keys, arr))

    @classmethod
    def prepare_input_list(cls, flight_dict: dict) -> list:
        """
        Utility function responsible for preparing input list for `StateVectorExtended` constructor sorted in proper order.

        Parameters
        ----------
        flight_dict : dict
            dictionary with all parameters needed to instantiate new `StateVectorExtended` object.

        Returns
        -------
        list
            Input list with items sorted in proper order, which corresponds with StateVectorExtended.keys list.

        """
        state_vector_index = {k: i for i, k in enumerate(StateVectorExtended.keys)}
        return [item[1] for item in sorted(flight_dict.items(), key=lambda item: state_vector_index[item[0]])]
