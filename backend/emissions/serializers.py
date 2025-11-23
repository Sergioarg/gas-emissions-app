# Django REST Framework
from rest_framework import serializers

# Internal
from emissions.helpers import validate_non_str_and_multiple_values


class EmissionSerializer(serializers.Serializer):

    year = serializers.IntegerField()
    emissions = serializers.FloatField()
    emission_type = serializers.CharField()
    country = serializers.CharField(source='country.name')
    activity = serializers.CharField()


class EmissionQueryParamSerializer(serializers.Serializer):
    string_regex = r'^[a-zA-Z\s]+$'
    activity = serializers.CharField(
        required=False,
        validators=[validate_non_str_and_multiple_values]
    )
    country = serializers.CharField(
        required=False,
        max_length=24,
        validators=[validate_non_str_and_multiple_values]
    )
    emission_type = serializers.CharField(
        required=False,
        max_length=24
    )

    def validate_query_params(self, query_params):
        serializer = EmissionQueryParamSerializer(data=query_params)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data
