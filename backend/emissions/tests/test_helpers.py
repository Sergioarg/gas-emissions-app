import pytest
from rest_framework.serializers import ValidationError

from emissions.helpers.query_parser import QueryParamParser
from emissions.helpers.validators import QueryParamValidator


class TestQueryParamParser:
    """Tests for QueryParamParser"""

    @pytest.mark.parametrize(
        "input_value,expected",
        [
            ("Japan", ["Japan"]),
            ("   Japan   ", ["Japan"]),
            ("Japan,Canada", ["Japan", "Canada"]),
            ("  Japan  ,  Canada  ", ["Japan", "Canada"]),
            ("", []),
            ("   ", []),
            ("Japan,,Canada", ["Japan", "Canada"]),
        ]
    )
    def test_parse_comma_separated_parametrized(
        self,
        input_value: str,
        expected: list[str],
    ):
        """Parametrized test for parse_comma_separated."""
        result = QueryParamParser.parse_comma_separated(input_value)
        assert result == expected


class TestQueryParamValidator:
    """Tests for QueryParamValidator"""

    def test_validate_numeric_value(
        self
    ):
        try:
            QueryParamValidator.validate_non_empty_and_non_numeric(
                "Japan, 123"
            )
        except ValidationError as e:
            assert str(e.detail[0]) == "Cannot be numeric"
