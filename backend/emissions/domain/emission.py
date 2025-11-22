from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from emissions.value_objects import CountryValueObject


@dataclass
class Emission:
    id: Optional[int]
    year: int
    emissions: float
    emission_type: str
    country: CountryValueObject
    activity: str
    created_at: datetime

    def is_recent(self) -> bool:
        """Business rule: Recent emission"""
        return self.year >= datetime.now().year - 5

    @classmethod
    def create(
            cls,
            year: int,
            emissions: float,
            emission_type: str,
            country_code: str,
            country_name: str,
            activity: str
    ) -> 'Emission':
        """Factory method with validation"""
        if year > datetime.now().year:
            raise ValueError("Invalid year")
        if emissions <= 0:
            raise ValueError("Emissions must be positive")

        return cls(
            id=None,
            year=year,
            emissions=emissions,
            emission_type=emission_type,
            country=CountryValueObject(country_name),
            activity=activity,
            created_at=datetime.now()
        )
