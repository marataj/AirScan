from typing import Any, Dict

from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView

from utils.planespotters_api import get_airplane_photo_url

from .forms import AircraftForm
from .models import AirplaneModel

# Create your views here.


class AircraftFormView(View):
    """
    Class that represents page with a aircraft search form.

    """

    def get(self, request):
        return render(request, "airplane_form.html", {"form": AircraftForm()})

    def post(self, request):
        form = AircraftForm(request.POST)
        if form.is_valid():
            icao24 = form.cleaned_data["icao24"].strip()
            records = AirplaneModel.objects.filter(icao24=icao24)
            if len(records) == 0:
                return render(
                    request,
                    "airplane_form.html",
                    {"form": AircraftForm(), "wrong_number": icao24},
                )
            return redirect(records[0].get_absolute_url())


class AircraftDetailView(DetailView):
    """
    Class that represents detail view of airplane model.

    """

    model = AirplaneModel
    template_name = "airplane_details.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["photo"] = get_airplane_photo_url(self.object.icao24)
        return context
