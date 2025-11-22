# Internal


def get_filtered_emissions(emissions, request):
    # TODO: buscar una mejor manera de hacer esto
    filter_actions = {
        'country': lambda emissions, value: [
            e for e in emissions if e.country.name == value
        ],
        'activity': lambda emissions, value: [
            e for e in emissions if value.lower() in e.activity.lower()
        ],
        'emission_type': lambda emissions, value: [
            e for e in emissions if e.emission_type == value
        ],
    }

    emissions = emissions.service.get_all_emissions()

    for param, filter_func in filter_actions.items():
        param_value = request.query_params.get(param)
        if param_value:
            emissions = filter_func(emissions, param_value)

    return emissions
