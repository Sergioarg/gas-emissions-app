# Standard Library
from typing import Dict, List, Optional

from emissions.domain.emission import Emission
# Internal
from emissions.domain.repository import EmissionRepositoryInterface
from emissions.helpers.query_parser import QueryParamParser


class EmissionApplicationService:

    def __init__(self, repository: EmissionRepositoryInterface):
        self.repository = repository

    def get_by_id(self, emission_id: int) -> Optional[Emission]:
        """Get an emission by its ID."""
        return self.repository.find_by_id(emission_id=emission_id)

    def get_all(self) -> list[Emission]:
        """Get all emissions."""
        return self.repository.find_all()

    def __parse_filter_param(
        self,
        query_params: Dict[str, str],
        param_name: str
    ) -> Optional[List[str]]:
        """Parse a filter parameter from query params."""
        param_value = query_params.get(param_name)
        if param_value and param_value.strip():
            return QueryParamParser.parse_comma_separated(param_value)
        return None

    def get_filtered(self, query_params: Dict[str, str]) -> list[Emission]:
        """Get emissions filtered by query parameters."""
        countries = self.__parse_filter_param(query_params, 'country')
        activities = self.__parse_filter_param(query_params, 'activity')
        emission_types = self.__parse_filter_param(
            query_params, 'emission_type'
        )

        return self.repository.find_filtered(
            countries=countries,
            activities=activities,
            emission_types=emission_types
        )
