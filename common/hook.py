
from flask import request, g, make_response

def api_before_request():
    if '/api' in request.path:
        return


def api_after_request(response):
    print(response)
    flask_resp = make_response(response.to_dict(), response.code)
    flask_resp.headers['content-type'] = "application/json"
    return flask_resp
