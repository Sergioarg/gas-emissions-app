from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Emission:
    id: Optional[int]
    year: int
    emissions: float
    emission_type: str
    country: str
    activity: str
    created_at: Optional[datetime]
