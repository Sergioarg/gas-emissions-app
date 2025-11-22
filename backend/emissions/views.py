"""Module EmissionViewSet"""

from rest_framework import viewsets
from emissions.models import Emission
from emissions.serializers import EmissionSerializer


class EmissionViewSet(viewsets.ModelViewSet):
    """Emission ViewSet with filtering capabilities"""

    queryset = Emission.objects.all().order_by("id")
    serializer_class = EmissionSerializer

    def get_queryset(self):
        """
        Optionally filter emissions by query parameters:
        - ?country=<country_name>
        - ?activity=<activity_name>
        - ?emission_type=<emission_type>
        """
        queryset = Emission.objects.all().order_by("id")

        # Filter by country
        country = self.request.query_params.get('country', None)
        if country is not None:
            queryset = queryset.filter(country__icontains=country)

        # Filter by activity
        activity = self.request.query_params.get('activity', None)
        if activity is not None:
            queryset = queryset.filter(activity__icontains=activity)

        # Filter by emission type
        emission_type = self.request.query_params.get('emission_type', None)
        if emission_type is not None:
            queryset = queryset.filter(emission_type__icontains=emission_type)

        return queryset
