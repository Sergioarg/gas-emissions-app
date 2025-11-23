# Internal
from rest_framework.serializers import ValidationError


def get_filtered_emissions(emissions, request):
    filter_actions = {
        'country': lambda emissions, values: [
            e for e in emissions
            if any(val.lower() in e.country.name.lower() for val in values)
        ],
        'activity': lambda emissions, values: [
            e for e in emissions
            if any(val.lower() in e.activity.lower() for val in values)
        ],
        'emission_type': lambda emissions, value: [
            e for e in emissions
            if e.emission_type == value
        ],
    }

    emissions = emissions.service.get_all_emissions()

    for param, filter_func in filter_actions.items():
        param_value = request.query_params.get(param)
        if param_value and param_value.strip():
            # Si es country o activity, separar por comas
            if param in ['country', 'activity']:
                values = [v.strip() for v in param_value.split(',')]
                emissions = filter_func(emissions, values)
            else:
                emissions = filter_func(emissions, param_value)

    return emissions


def validate_non_str_and_multiple_values(value: str) -> str:
    if not value or not value.strip():
        raise ValidationError("Cannot be empty")

    values = [v.strip() for v in value.split(',')]

    for val in values:
        if not val:
            raise ValidationError(
                "Empty value in comma-separated list"
            )

        if val.isdigit():
            raise ValidationError("Cannot be only numbers")

    return value
