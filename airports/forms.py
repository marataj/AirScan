from django import forms
from django.forms import DateTimeInput


class AirportFlights(forms.Form):
    type = forms.ChoiceField(choices=(("1", "Departures"), ("2", "Arrivals")))
    begin_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local'
        })
    )
    end_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        begin = cleaned_data.get("begin_time")
        end = cleaned_data.get("end_time")
        # validation of form
        
