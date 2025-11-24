# Standard Library
from typing import List

# Django
from django.db.models import Q

from emissions.domain.emission import Emission
# Internal
from emissions.domain.repository import EmissionRepositoryInterface
from emissions.models import Emission as DjangoEmission


class DjangoEmissionRepository(EmissionRepositoryInterface):
    """Repository for Django emissions."""

    def find_all(self) -> list[Emission]:
        django_emissions = DjangoEmission.objects.all()
        return self._convert_to_domain(django_emissions)

    def find_by_id(self, emission_id: int) -> Emission:
        django_emission = DjangoEmission.objects.get(id=emission_id)
        return self._to_domain(django_emission)

    def find_filtered(
        self,
        countries: List[str] = None,
        activities: List[str] = None,
        emission_types: List[str] = None
    ) -> list[Emission]:
        """Find emissions with multiple filters applied at DB level."""
        queryset = DjangoEmission.objects.all()

        if countries:
            country_q = Q()
            for country in countries:
                country_q |= Q(country__icontains=country)
            queryset = queryset.filter(country_q)

        if activities:
            activity_q = Q()
            for activity in activities:
                activity_q |= Q(activity__icontains=activity)
            queryset = queryset.filter(activity_q)

        if emission_types:
            queryset = queryset.filter(emission_type__in=emission_types)

        return self._convert_to_domain(list(queryset))

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
