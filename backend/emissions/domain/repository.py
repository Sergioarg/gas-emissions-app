# Standard Library
from abc import ABC, abstractmethod
from typing import List, Optional

# Internal
from emissions.domain.emission import Emission


class EmissionRepositoryInterface(ABC):

    @abstractmethod
    def find_by_id(self, emission_id: int) -> Optional[Emission]:
        pass

    @abstractmethod
    def find_all(self) -> List[Emission]:
        pass

    @abstractmethod
    def find_by_country(self, country_name: str) -> List[Emission]:
        pass

    @abstractmethod
    def find_by_activity(self, activity: str) -> List[Emission]:
        pass

    @abstractmethod
    def find_by_emissions_type(self, emission_type: str) -> List[Emission]:
        pass
