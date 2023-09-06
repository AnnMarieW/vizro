"""Helper functions for models inside form folder."""
from vizro._constants import ALL_OPTION
from vizro.models.types import OptionsType


def get_options_and_default(options: OptionsType, multi: bool = False):
    """Gets list of full options and default value based on user input type of `options`."""
    if multi:
        if all(isinstance(option, dict) for option in options):
            options = [{"label": ALL_OPTION, "value": ALL_OPTION}, *options]
        else:
            options = [ALL_OPTION, *options]

    if all(isinstance(option, dict) for option in options):
        default_value = options[0]["value"]  # type: ignore[index]
    else:
        default_value = options[0]

    return options, default_value