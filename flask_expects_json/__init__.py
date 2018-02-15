from functools import wraps
from flask import request, g, abort

from jsonschema import validate, ValidationError
from .default_validator import DefaultValidatingDraft4Validator


def expects_json(schema=None, force=False, fill_defaults=True):
    if schema is None:
        schema = dict()

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json(force=force)

            if data is None:
                return abort(400, 'This view expects mimetype application/json.')

            try:
                if fill_defaults:
                    DefaultValidatingDraft4Validator(schema).validate(data)
                else:
                    validate(data, schema)
            except ValidationError as e:
                return abort(400, e.message)

            g.data = data
            return f(*args, **kwargs)
        return decorated_function
    return decorator
