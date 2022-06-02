# coding=utf-8

from flask import request

def validator(schema):
    def check_json(f):
        def wrap_handler(*args, **kwargs):
            data = request.get_json(force=True)  # type: ignore

            return f(*args, **kwargs)
        return wrap_handler

    return check_json
