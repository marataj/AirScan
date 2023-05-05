from django import forms


class AircraftForm(forms.Form):
    """
    Class that represents aircraft search form.

    """
    icao24 = forms.CharField(max_length=10)
