# coding=utf-8

import json

from flask import make_response


def wrap_response(f):
    def format_response(*args, **kwargs):
        resp = f(*args, **kwargs)
        flask_resp = make_response(resp.to_dict(), resp.code)
        flask_resp.headers["content-type"] = "application/json"
        return flask_resp

    return format_response


class Response(object):
    def __init__(self, code, message, data):
        self.code = code
        self.message = message
        self.data = data

    def to_dict(self):
        return {"code": self.code, "message": self.message, "data": self.data}


class OK(Response):
    def __init__(self, message, data):
        super(OK, self).__init__(200, message, data)


class BadRequest(Response):
    def __init__(self, message):
        super(BadRequest, self).__init__(400, message, None)


class InternalServerError(Response):
    def __init__(self, message):
        super(InternalServerError, self).__init__(500, message, None)


class NotFound(Response):
    def __init__(self, message):
        super(NotFound, self).__init__(404, message, None)


class Forbidden(Response):
    def __init__(self, message):
        super(Forbidden, self).__init__(403, message, None)


class Raw:
    def __init__(self, code, raw_data):
        if type(raw_data) == dict or type(raw_data) == list:
            self.data = raw_data
            self.code = code
        else:
            raise TypeError("Raw Response Only Support Dict or List Object")

    def to_dict(self):
        return json.dumps(self.data)
