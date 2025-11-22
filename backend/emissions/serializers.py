from rest_framework import serializers
from emissions.models import Emission


class EmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emission
        fields = "__all__"
