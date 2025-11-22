from dataclasses import dataclass


@dataclass(frozen=True)
class CountryValueObject:
    name: str

    def __post_init__(self):
        if not self.name:
            raise ValueError("Name are required")

    @classmethod
    def from_name(cls, country_name: str) -> 'CountryValueObject':
        return cls(name=country_name)
