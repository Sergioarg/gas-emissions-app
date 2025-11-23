import pytest
from emissions.models import Emission
from rest_framework.test import APIClient


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


def extract_field_from_response_data(
    response_data: list[dict],
    field_name: str
) -> list[str]:
    """Extract values from a field in the response data"""

    return [item.get(field_name) for item in response_data]
