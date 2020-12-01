import functools

from marshmallow import ValidationError
from flask import request

from frank_proctor import responses


def validate_request(schema):
    def decorator(fn):
        @functools.wraps(fn)
        def decorated():
            args = request.json
            if args is None:
                return responses.invalid_arguments(
                    "invalid content type")

            try:
                result = schema().load(args)
                return fn(result)
            except ValidationError as error:
                return responses.invalid_arguments(error.messages)

            return fn(args)
        return decorated

    return decorator
