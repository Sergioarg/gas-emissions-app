"""
Responsibility: Parse and normalize query parameter values.
Single Responsibility: Handle comma-separated value parsing.
"""
from typing import List


class QueryParamParser:
    """Parse and normalize query parameter values."""

    @staticmethod
    def parse_comma_separated(value: str) -> List[str]:
        """
        Parse comma-separated string into list of trimmed values.

        Args:
            value: Comma-separated string (e.g., "Japan,Canada")

        Returns:
            List of trimmed, non-empty values

        Example:
            >>> QueryParamParser.parse_comma_separated("Japan,Canada, ")
            ['Japan', 'Canada']
        """
        if not value or not value.strip():
            return []

        return [v.strip() for v in value.split(',') if v.strip()]
