# Standard Library
from emissions.domain.emission import Emission
# Internal
from emissions.domain.repository import EmissionRepositoryInterface


class EmissionApplicationService:

    def __init__(self, repository: EmissionRepositoryInterface):
        self.repository = repository

    def find_by_id(self, emission_id: int) -> Emission:
        return self.repository.find_by_id(emission_id)

    def get_all_emissions(self) -> list[Emission]:
        return self.repository.find_all()

    def get_emissions_by_country(self, country_name: str) -> list[Emission]:
        return self.repository.find_by_country(country_name)

    def get_emissions_by_activity(self, activity: str) -> list[Emission]:
        return self.repository.find_by_activity(activity)

    def get_emissions_by_type(
        self,
        emission_type: str,
    ) -> list[Emission]:
        return self.repository.find_by_type(emission_type)
