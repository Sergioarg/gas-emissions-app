# Internal
from rest_framework.serializers import ValidationError
# TODO: Refactorizar ESTE ARCHIVO


# Esta funcion se esta utilizando en muchos lugares (así no debe ser)
def split_comma_separated_values(value: str) -> list[str]:
    return [v.strip() for v in value.split(',') if v.strip()]


class CommaSeparatedFilter:
    @staticmethod
    def filter_in(emissions: list, field_name: str, values: list[str]) -> list:
        if not values:
            return emissions

        filtered = []
        for emission in emissions:
            field_value = getattr(emission, field_name, None)
            if field_value:
                # Case-insensitive matching
                if any(
                    val.lower() in str(field_value).lower()
                    for val in values
                ):
                    filtered.append(emission)
        return filtered


def get_filtered_emissions(emissions, request):
    filter_actions = {
        'country': lambda emissions, values:
        CommaSeparatedFilter.filter_in(
            emissions, 'country', values
        ),
        'activity': lambda emissions, values:
        CommaSeparatedFilter.filter_in(
            emissions, 'activity', values
        ),
        'emission_type': lambda emissions, values:
        CommaSeparatedFilter.filter_in(
            emissions, 'emission_type', values
        ),
    }

    emissions = emissions.service.get_all()

    for param, filter_func in filter_actions.items():
        param_value = request.query_params.get(param)
        if param_value and param_value.strip():
            values = split_comma_separated_values(param_value)
            emissions = filter_func(emissions, values)

    return emissions


def validate_non_str_and_multiple_values(value: str) -> str:
    if not value or not value.strip():
        raise ValidationError("Cannot be empty")

    values = split_comma_separated_values(value)

    for val in values:
        if not val:
            raise ValidationError(
                "Empty value in comma-separated list"
            )

        if val.isdigit():
            raise ValidationError("Cannot be only numbers")

    return value
