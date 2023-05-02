from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError


class AirportFlightsForm(forms.Form):
    """
    Class representing form responsible to collect data to generate airport flight list

    """

    type = forms.ChoiceField(choices=(("1", "Departures"), ("2", "Arrivals")))
    begin_time = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )
    end_time = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )

    def clean(self):
        """
        Method to validate form.

        Raises
        ------
        ValidationError
            Raises in case of invalid data.

        """
        cleaned_data = super().clean()
        begin = cleaned_data.get("begin_time")
        end = cleaned_data.get("end_time")
        if end - begin > timedelta(days=7):
            raise ValidationError("The time period is greather than 7 days!")
        if end - begin < timedelta(days=0):
            raise ValidationError("The end date is earlier than the begin date!")
