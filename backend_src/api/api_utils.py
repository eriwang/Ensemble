from functools import wraps

from flask import jsonify


class BadRequestException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


def api_jsonify_errors(fxn):
    @wraps(fxn)
    def wrapper(*args, **kwargs):
        try:
            return fxn(*args, **kwargs)
        except BadRequestException as e:
            return jsonify({'error': e.message}), 400

    return wrapper


def validate_and_load_params(params, key_to_types, optional_key_to_types=None):
    received_keys = sorted(params.keys())
    if optional_key_to_types is None:
        expected_keys = sorted(key_to_types.keys())
        if received_keys != expected_keys:
            raise BadRequestException(f'Expected keys {expected_keys}, received {received_keys} instead')
    else:
        required_keys_set = set(key_to_types.keys())
        optional_keys_set = set(optional_key_to_types.keys())
        if len(required_keys_set & optional_keys_set) > 0:
            raise ValueError('Keys in required/ optional key_to_types must be mutually exclusive')

        received_keys_set = set(received_keys)
        if len(required_keys_set - received_keys_set) > 0:
            raise BadRequestException(f'Keys {sorted(required_keys_set)} are required, received {received_keys}')

        supported_keys_set = required_keys_set.union(optional_keys_set)
        if len(received_keys_set - supported_keys_set) > 0:
            raise BadRequestException(f'Only keys {sorted(supported_keys_set)} are supported, received {received_keys}')

        present_optional_key_types = {key: value_type for key, value_type in optional_key_to_types.items()
                                      if key in params}
        key_to_types = {**key_to_types, **present_optional_key_types}

    return _validate_types_and_load_params(params, key_to_types)


def _validate_types_and_load_params(params, key_to_types):
    type_errors = []
    loaded_params = {}
    for key, value_type in key_to_types.items():
        value = params[key]
        loaded_value = None
        if isinstance(value_type, str):
            loaded_value = _try_load_custom_type(value, value_type)
        elif isinstance(value, value_type):
            loaded_value = value

        if loaded_value is None:
            type_errors.append(f'{key}:{value_type}')
        else:
            loaded_params[key] = loaded_value

    if len(type_errors) > 0:
        type_errors_str = ', '.join(type_errors)
        raise BadRequestException(f'Type mismatch(es), for following params, expected: {type_errors_str}')

    return loaded_params


def _try_load_custom_type(value, value_type):
    if value_type == 'boolstr':
        if value == 'true':
            return True
        if value == 'false':
            return False
        return None

    raise ValueError(f'Unknown value_type "{value_type}"')
