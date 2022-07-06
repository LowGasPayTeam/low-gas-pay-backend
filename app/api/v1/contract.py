# coding=utf-8

from flask import current_app, request
from flask_restful import Resource

from app.models.contract import Contract
from common import response
from common.validator import validator

POST_SCHEMA = {
    "type": "object",
    "properties": {
        "contract": {"type": "string", "pattern": "^0x[a-fA-F0-9]{40}$"},
    },
    "required": ["contract"],
}


class ContractListApi(Resource):
    @response.wrap_response
    def get(self):
        try:
            contracts = Contract.query.all()
            values = [item.contract for item in contracts]

        except Exception as e:
            current_app.logger.error(f"Get Contracts Error: {e}")
            return response.InternalServerError(f"Get Contracts Error: {e}")
        return response.Raw(200, values)

    @response.wrap_response
    @validator(POST_SCHEMA)
    def post(self):
        data = request.get_json(force=True)  # type: ignore
        user_contract = data.get("contract")
        try:
            contract = Contract(contract=user_contract)
            contract.save()
        except Exception as e:
            current_app.logger.error(f"Save Contracts Error: {e}")
            return response.InternalServerError(f"Save Contracts Error: {e}")
        return response.OK(None, contract.as_dict())


class ContractApi(Resource):
    @response.wrap_response
    def get(self, contract_hash):
        try:
            contract = Contract.query.filter_by(contract=contract_hash).first()
        except Exception:
            current_app.logger.error(f"Contract {contract_hash} Not Found")
            return response.NotFound(f"Contract {contract_hash} Not Found")
        if not contract:
            return response.NotFound(f"Contract {contract_hash} Not Found")
        return response.OK(None, contract.as_dict())

    @response.wrap_response
    def delete(self, contract_hash):
        try:
            contract = Contract.query.filter_by(contract=contract_hash).first()
        except Exception:
            current_app.logger.error(f"Delete Contract {contract_hash} Error")
            return response.NotFound(f"Delete Contract {contract_hash} Error")

        if not contract:
            return response.NotFound(f"Contract {contract_hash} Not Found")

        try:
            contract.delete(force=True)
        except Exception as e:
            current_app.logger.error(f"Delete Contract {contract_hash} Error: {e}")
            return response.InternalServerError(
                f"Delete NFT Order {contract_hash} Error: {e}"
            )

        return response.OK(f"Contract {contract_hash} Deleted", None)
