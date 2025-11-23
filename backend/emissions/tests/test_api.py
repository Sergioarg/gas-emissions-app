import pytest
from rest_framework import status

# Helpers
from emissions.tests.conftest import extract_and_normalize_field


@pytest.mark.django_db
class TestEmissionAPI:
    BASE_URL = "/api/emissions/"

    def test_list_emissions_empty_success(self, api_client):
        response = api_client.get(self.BASE_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_list_emissions_success(self, api_client, sample_emissions):
        response = api_client.get(self.BASE_URL)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        keys = response.data[0].keys()
        expected_keys = [
            "year",
            "emissions",
            "emission_type",
            "country",
            "activity",
        ]
        assert set(keys) == set(expected_keys)

    @pytest.mark.parametrize(
        "number_results,country",
        [
            (2, "Japan"),
            (3, "Japan,Canada"),
        ]
    )
    def test_filter_by_country_success(
        self,
        api_client,
        sample_emissions,
        number_results,
        country
    ):
        response = api_client.get(f"{self.BASE_URL}?country={country}")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == number_results
        (
            countries_response,
            countries_query_params
        ) = extract_and_normalize_field(
            response.data, "country", country
        )
        for country in countries_query_params:
            assert country in countries_response

    @pytest.mark.parametrize(
        "number_results,activity",
        [
            (1, "Industrial Processes"),
            (2, "Industrial Processes, Transportation"),
        ]
    )
    def test_filter_by_activity_success(
        self,
        api_client,
        sample_emissions,
        number_results,
        activity
    ):
        response = api_client.get(f"{self.BASE_URL}?activity={activity}")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == number_results
        (
            activities_response,
            activities_query_params
        ) = extract_and_normalize_field(
            response.data, "activity", activity
        )
        for activity in activities_query_params:
            assert activity in activities_response

    @pytest.mark.parametrize(
        "number_results,emission_type",
        [
            (2, "CO2"),
            (3, "CO2, CH4"),
        ]
    )
    def test_filter_by_emission_type_success(
        self,
        api_client,
        sample_emissions,
        number_results,
        emission_type
    ):
        response = api_client.get(
            f"{self.BASE_URL}?emission_type={emission_type}"
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == number_results
        (
            emission_types_response,
            emission_types_query_params
        ) = extract_and_normalize_field(
            response.data, "emission_type", emission_type
        )
        for emission_type in emission_types_query_params:
            assert emission_type in emission_types_response

    @pytest.mark.parametrize(
        "param,value",
        [
            ("country", "123"),
            ("country", "Japan,123"),
            ("activity", "123"),
            ("activity", "Industrial Processes,123"),
        ]
    )
    def test_invalid_filter_by_number(
        self, api_client, param, value
    ):
        response = api_client.get(f"{self.BASE_URL}?{param}={value}")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    # TODO: Check test for invalid country empty
    # def test_filter_invalid_country_empty(self, api_client):
    #     response = api_client.get(f"{self.BASE_URL}?country=")
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert "error" in response.data
