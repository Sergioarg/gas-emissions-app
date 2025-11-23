# Django REST Framework
from rest_framework import serializers

# Internal
from emissions.helpers.validators import QueryParamValidator


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

    def validate_query_params(self, query_params):
        serializer = EmissionQueryParamSerializer(data=query_params)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data
