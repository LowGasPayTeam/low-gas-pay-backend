# coding=utf-8

from app.api import rest_api_bp


def register_bp(app):
    app.register_blueprint(rest_api_bp, url_prefix="/api")

    print(app.blueprints)
