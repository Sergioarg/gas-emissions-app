# Internal
from emissions.helpers.query_parser import QueryParamParser
# DRF
from rest_framework.serializers import ValidationError


class QueryParamValidator:
    """Validate query parameter values."""

    @staticmethod
    def validate_non_empty_and_non_numeric(query_params: str) -> None:
        """
        Validate that value is not empty and not purely numeric.

        Args:
            value: Query parameter value to validate

        Raises:
            ValidationError: If value is empty or purely numeric

        """
        if not query_params or not query_params.strip():
            raise ValidationError("Cannot be empty")

        parsed_values = QueryParamParser.parse_comma_separated(query_params)

        for val in parsed_values:
            if not val:
                raise ValidationError("Empty value in comma-separated list")

            if val.isdigit():
                raise ValidationError("Does not support numeric values")
