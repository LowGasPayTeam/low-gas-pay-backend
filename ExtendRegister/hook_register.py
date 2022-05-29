# coding=utf-8

from common.hook import api_after_request

def register_hook(app):
    for bp in app.blueprints.values():
        bp.after_request(api_after_request)
