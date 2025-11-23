"""
Orchestrate filtering operations.
"""
from typing import List, Any
from rest_framework.request import Request

from emissions.helpers.query_parser import QueryParamParser
from emissions.helpers.emission_filter import EmissionFilter


class EmissionFilterService:
    """Service to apply multiple filters to emissions."""

    FILTER_MAPPING = {
        'country': EmissionFilter.filter_by_country,
        'activity': EmissionFilter.filter_by_activity,
        'emission_type': EmissionFilter.filter_by_emission_type,
    }

    @classmethod
    def apply_filters(
        cls,
        emissions: List[Any],
        request: Request,
    ) -> List[Any]:
        """
        Apply all query parameter filters to emissions list.

        Args:
            emissions: List of emission objects to filter
            request: Django REST Framework request object

        Returns:
            Filtered list of emissions
        """
        filtered_emissions = emissions

        for param_name, filter_func in cls.FILTER_MAPPING.items():
            param_value = request.query_params.get(param_name)
            if not param_value or not param_value.strip():
                continue

            # Parse comma-separated values
            if param_name in ['country', 'activity', 'emission_type']:
                values = QueryParamParser.parse_comma_separated(param_value)
            else:
                # For emission_type, also support comma-separated
                values = QueryParamParser.parse_comma_separated(param_value)

            if values:
                filtered_emissions = filter_func(filtered_emissions, values)

        return filtered_emissions
