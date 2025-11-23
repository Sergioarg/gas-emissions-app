from rest_framework.serializers import ValidationError
from emissions.helpers.query_parser import QueryParamParser


class QueryParamValidator:
    """Validate query parameter values."""

    @staticmethod
    def validate_non_empty_and_non_numeric(value: str) -> None:
        """
        Validate that value is not empty and not purely numeric.

        Args:
            value: Query parameter value to validate

        Raises:
            ValidationError: If value is empty or purely numeric

        """
        if not value or not value.strip():
            raise ValidationError("Cannot be empty")

        parsed_values = QueryParamParser.parse_comma_separated(value)

        for val in parsed_values:
            if not val:
                raise ValidationError("Empty value in comma-separated list")

            if val.isdigit():
                raise ValidationError("Cannot be numeric")
