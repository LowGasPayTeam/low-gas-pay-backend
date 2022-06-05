# coding=utf-8

from flask import Blueprint
from flask_restful import Api

from .v1.token import TokenListApi, TokenApi
from .v1.gas import GasApi

rest_api_bp = Blueprint("api", __name__)
api = Api(rest_api_bp)

api.add_resource(TokenListApi, "/v1/tokens", endpoint="tokens")
api.add_resource(TokenApi, "/v1/tokens/<int:id>", endpoint="token")
api.add_resource(GasApi, "/v1/gas", endpoint="gas")
