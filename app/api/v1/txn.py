# coding=utf-8
# pyright: reportUndefinedVariable=false, reportGeneralTypeIssues=false
#

from flask import request
from flask_restful import Resource
from app.models.token_transaction import TokenTxn
from common import response


class TxnApi(Resource):

    @response.wrap_response
    def get(self, id):
        try:
            token_txn = TokenTxn.query.get(id)
        except Exception as error:
            return response.InternalServerError(f"Get Token Transaction {id} Error: {error}")

        if not token_txn:
            return response.NotFound(f"Token Transaction {id} Not Found")
        return response.OK("Successful", token_txn.as_dict())

    @response.wrap_response
    def put(self, id):
        try:
            token_txn = TokenTxn.query.get(id)
        except Exception as error:
            return response.InternalServerError(f"Get Token Transaction {id} Error: {error}")
        if not token_txn:
            return response.NotFound(f"Token Transaction {id} Not Found")

        data = request.get_json(force=True)  # type: ignore
        if not data:
            return response.BadRequest("Required Data Missing")

        try:
            token_txn_dict = token_txn.as_dict()
            for key, value in data.items():
                if key in token_txn_dict:
                    setattr(token_txn, key, value)
            token_txn.update()
        except Exception as error:
            return response.InternalServerError(
                f"Token Transaction {id} Update Failed, Error: {error}"
            )
        return response.OK(f"Token Transaction {id} Update Success", None)
