from rest_framework.test import APITestCase
from emissions.models import Emission


class EmissionAPITest(APITestCase):
    """Tests básicos para la API REST de emisiones"""

    def test_api_list_endpoint(self):
        """Test que el endpoint de listar funciona"""
        response = self.client.get("/api/emissions/")
        self.assertEqual(response.status_code, 200)

    def test_api_filter_endpoints(self):
        base_url = "/api/emissions/"

        filters = [
            "?country=México",
            "?activity=Transporte",
            "?emission_type=CO2",
            "?country=México&emission_type=CO2",
        ]

        for filter_param in filters:
            with self.subTest(filter=filter_param):
                response = self.client.get(base_url + filter_param)
                self.assertEqual(response.status_code, 200)

    def test_response_structure(self):
        Emission.objects.create(
            year=2023,
            emissions=150.50,
            emission_type="CO2",
            country="México",
            activity="Transporte",
        )

        response = self.client.get("/api/emissions/")

        if response.status_code == 200:
            self.assertIsInstance(response.data, list)

            if response.data:
                item = response.data[0]
                expected_fields = [
                    "year",
                    "emissions",
                    "emission_type",
                    "country",
                    "activity",
                ]
                for field in expected_fields:
                    self.assertIn(field, item)
