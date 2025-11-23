"""
Filter emissions by different criteria.
"""
from typing import List, Any


class EmissionFilter:
    """Filter emissions by various criteria."""

    @staticmethod
    def filter_by_field(
        emissions: List[Any],
        field_name: str,
        values: List[str],
        match_type: str = "contains"
    ) -> List[Any]:
        """
        Filter emissions by field value with case-insensitive matching.

        Args:
            emissions: List of emission objects
            field_name: Name of the field to filter by
            values: List of values to match against
            match_type: "contains" (default) or "exact"

        Returns:
            Filtered list of emissions
        """
        if not values:
            return emissions

        filtered = []
        for emission in emissions:
            field_value = getattr(emission, field_name, None)
            if not field_value:
                continue

            field_str = str(field_value).lower()
            matches = [
                val.lower() in field_str if match_type == "contains"
                else val.lower() == field_str
                for val in values
            ]

            if any(matches):
                filtered.append(emission)

        return filtered

    @staticmethod
    def filter_by_country(
        emissions: List[Any],
        countries: List[str],
    ) -> List[Any]:
        """Filter emissions by country name(s)."""
        return EmissionFilter.filter_by_field(
            emissions, 'country', countries, match_type="contains"
        )

    @staticmethod
    def filter_by_activity(
        emissions: List[Any],
        activities: List[str],
    ) -> List[Any]:
        """Filter emissions by activity type(s)."""
        return EmissionFilter.filter_by_field(
            emissions, 'activity', activities, match_type="contains"
        )

    @staticmethod
    def filter_by_emission_type(
        emissions: List[Any],
        emission_types: List[str],
    ) -> List[Any]:
        """Filter emissions by emission type(s)."""
        return EmissionFilter.filter_by_field(
            emissions, 'emission_type', emission_types, match_type="exact"
        )
