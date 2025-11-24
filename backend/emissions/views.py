# Internal
from emissions.app.service import EmissionApplicationService
from emissions.infrastructure.django_repository import DjangoEmissionRepository
from emissions.models import Emission as DjangoEmission
from emissions.serializers import (
    EmissionQueryParamSerializer,
    EmissionSerializer,
)
# DRF
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response


class EmissionViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = DjangoEmission.objects.none()
    serializer_class = EmissionSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        repository = DjangoEmissionRepository()
        self.service = EmissionApplicationService(repository)

    def __get_query_params_dict(self, request: Request) -> dict[str, str]:
        """Get query parameters as a dictionary."""
        return {
            key: value[0] if isinstance(value, list) else value
            for key, value in request.query_params.items()
        }

    def list(self, request):
        """GET /api/emissions/ """
        try:
            query_serializer = EmissionQueryParamSerializer(
                data=request.query_params
            )
            query_serializer.is_valid(raise_exception=True)

            query_params_dict = self.__get_query_params_dict(request)

            emissions = self.service.get_filtered(query_params_dict)

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
