import pytest
from emissions.models import Emission
from rest_framework.test import APIClient
from emissions.helpers.query_parser import QueryParamParser


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_emissions():
    """Fixture con datos iniciales para todos los tests"""
    emissions = [
        Emission.objects.create(
            year=2020,
            emissions=100.5,
            emission_type="CO2",
            country="Japan",
            activity="Transportation"
        ),
        Emission.objects.create(
            year=2021,
            emissions=200.3,
            emission_type="CH4",
            country="Canada",
            activity="Agriculture"
        ),
        Emission.objects.create(
            year=2022,
            emissions=150.0,
            emission_type="CO2",
            country="Japan",
            activity="Industrial Processes"
        ),
        Emission.objects.create(
            year=2020,
            emissions=75.2,
            emission_type="N2O",
            country="Germany",
            activity="Waste"
        ),
    ]
    return emissions


@pytest.fixture
def single_emission():
    """Fixture con un solo registro para tests específicos"""
    return Emission.objects.create(
        year=2023,
        emissions=300.0,
        emission_type="SF6",
        country="United States",
        activity="Energy Production"
    )


def extract_and_normalize_field(
    response_data: list[dict],
    field_name: str,
    field_value: str
) -> tuple[list[str], list[str]]:
    """Extract values from a field in the response data"""
    response_values = [item.get(field_name) for item in response_data]
    query_params_values = QueryParamParser.parse_comma_separated(
        field_value
    )

    return response_values, query_params_values
