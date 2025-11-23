# Internal
from emissions.helpers.validators import QueryParamValidator
# DRF
from rest_framework import serializers


class EmissionSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    emissions = serializers.FloatField()
    emission_type = serializers.CharField()
    country = serializers.CharField()
    activity = serializers.CharField()


class EmissionQueryParamSerializer(serializers.Serializer):
    activity = serializers.CharField(
        required=False,
        validators=[QueryParamValidator.validate_non_empty_and_non_numeric]
    )
    country = serializers.CharField(
        required=False,
        max_length=24,
        validators=[QueryParamValidator.validate_non_empty_and_non_numeric]
    )
    emission_type = serializers.CharField(
        required=False,
        max_length=24
    )
