# coding=utf-8

import functools
from flask import request
from jsonschema import validate
from jsonschema.exceptions import SchemaError, ValidationError
from common.response import *


def validator(schema):
    def check_json(f):
        @functools.wraps(f)
        def wrap_handler(*args, **kwargs):
            data = request.get_json(force=True)  # type: ignore
            try:
                validate(instance=data, schema=schema)
            except SchemaError as e:
                return InternalServerError(f"Schema Error: {e}")
            except ValidationError as e:
                return BadRequest(f"Bad Request: {e}")
            return f(*args, **kwargs)
        return wrap_handler
    return check_json
