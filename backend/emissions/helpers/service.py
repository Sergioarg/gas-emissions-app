from emissions.helpers.filter_service import EmissionFilterService
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request


def get_filtered_emissions(viewset_instance: ViewSet, request: Request):
    """
    Get and filter emissions based on query parameters.

    Note: This function now only handles filtering, not data retrieval.
    The viewset should retrieve data first, then pass it here.
    """
    # Get all emissions from service
    emissions = viewset_instance.service.get_all()

    # Apply filters
    return EmissionFilterService.apply_filters(emissions, request)
