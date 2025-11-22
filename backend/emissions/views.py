# Django REST Framework
from rest_framework import viewsets

# Internal
from emissions.app.service import EmissionApplicationService
from emissions.infrastructure.django_emission_repository import (
    DjangoEmissionRepository
)
from emissions.models import Emission as DjangoEmission
from emissions.serializers import EmissionSerializer
from emissions.helpers import get_filtered_emissions
from rest_framework.response import Response


class EmissionViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = DjangoEmission.objects.none()
    serializer_class = EmissionSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        repository = DjangoEmissionRepository()
        self.service = EmissionApplicationService(repository)

    def list(self, request):
        """GET /api/emissions/ """
        emissions = get_filtered_emissions(self, request)
        return Response(self.get_serializer(emissions, many=True).data)
