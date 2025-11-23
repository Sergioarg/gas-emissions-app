# Django REST Framework
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

# Internal
from emissions.app.service import EmissionApplicationService
from emissions.helpers import get_filtered_emissions
from emissions.infrastructure.django_emission_repository import \
    DjangoEmissionRepository
from emissions.models import Emission as DjangoEmission
from emissions.serializers import (
    EmissionQueryParamSerializer,
    EmissionSerializer,
)


class EmissionViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = DjangoEmission.objects.none()
    serializer_class = EmissionSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        repository = DjangoEmissionRepository()
        self.service = EmissionApplicationService(repository)

    def list(self, request):
        """GET /api/emissions/ """
        try:
            query_serializer = EmissionQueryParamSerializer(
                data=request.query_params
            )
            query_serializer.is_valid(raise_exception=True)
            emissions = get_filtered_emissions(self, request)

            serializer = self.get_serializer(emissions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({
                "error": "Invalid query parameters",
                "details": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "error": "Internal server error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
