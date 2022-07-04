# coding=utf-8

import requests
from flask import current_app
from flask_restful import Resource

from common import response


class GasApi(Resource):
    @response.wrap_response
    def get(self):
        gasRes = get_gas()
        if gasRes is None:
            current_app.logger.error("Get Gas Failed")
            return response.InternalServerError("Get Gas Failed")
        low, mid, high, suggest = gas_level(gasRes)
        gas = dict(low=low, mid=mid, high=high, suggest=suggest)
        return response.OK("Success", gas)


def get_gas():
    api_key = current_app.config["ETHSCAN_API_KEY"]
    gas_oracle_path = current_app.config["ETHSCAN_ORACLE_PATH"]
    timeout = current_app.config["ETHSCAN_TIMEOUT"]

    resp = requests.get(gas_oracle_path + api_key, timeout=int(timeout)).json()
    if resp["status"] == "1" and resp["message"] == "OK":
        return resp["result"]
    else:
        return None


def gas_level(gasResult):
    return (
        gasResult["SafeGasPrice"],
        gasResult["ProposeGasPrice"],
        gasResult["FastGasPrice"],
        gasResult["suggestBaseFee"],
    )
