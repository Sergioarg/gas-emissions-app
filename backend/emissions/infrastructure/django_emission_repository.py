from emissions.domain.emission import Emission
from emissions.domain.repository import EmissionRepositoryInterface

from emissions.models import Emission as DjangoEmission


class DjangoEmissionRepository(EmissionRepositoryInterface):

    def find_all(self) -> list[Emission]:
        django_emissions = DjangoEmission.objects.all()
        return self._convert_to_domain(django_emissions)

    def find_by_id(self, emission_id: int) -> Emission:
        django_emission = DjangoEmission.objects.get(id=emission_id)
        return self._to_domain(django_emission)

    def find_by_country(self, country_code: str) -> list[Emission]:
        django_emissions = DjangoEmission.objects.filter(country=country_code)
        return self._convert_to_domain(django_emissions)

    def find_by_activity(self, activity: str) -> list[Emission]:
        django_emissions = DjangoEmission.objects.filter(activity=activity)
        return self._convert_to_domain(django_emissions)

    def find_by_type(self, emission_type: str) -> list[Emission]:
        django_emissions = DjangoEmission.objects.filter(
            emission_type=emission_type
        )
        return self._convert_to_domain(django_emissions)

    def _to_domain(self, django_emission: DjangoEmission) -> Emission:
        return Emission(
            id=django_emission.id,
            year=django_emission.year,
            emissions=float(django_emission.emissions),
            emission_type=django_emission.emission_type,
            country=django_emission.country,
            activity=django_emission.activity,
            created_at=django_emission.created_at
        )

    def _convert_to_domain(
        self,
        django_emissions: list[DjangoEmission]
    ) -> list[Emission]:
        return [self._to_domain(emission) for emission in django_emissions]
