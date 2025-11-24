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
    def find_filtered(
        self,
        countries: List[str] = None,
        activities: List[str] = None,
        emission_types: List[str] = None
    ) -> List[Emission]:
        """Find emissions with filters applied at DB level."""
        pass
