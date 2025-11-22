from rest_framework import serializers


class EmissionSerializer(serializers.Serializer):

    year = serializers.IntegerField()
    emissions = serializers.FloatField()
    emission_type = serializers.CharField()
    country = serializers.CharField(source='country.name')
    activity = serializers.CharField()
