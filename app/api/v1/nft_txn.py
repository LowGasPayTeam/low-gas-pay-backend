# coding=utf-8
# pyright: reportUndefinedVariable=false, reportGeneralTypeIssues=false
#

from flask import request
from flask_restful import Resource
from app.models.nft_transaction import NFTTxn
from common import response


class NFTTxnApi(Resource):

    @response.wrap_response
    def get(self, id):
        try:
            nft_txn = NFTTxn.query.get(id)
        except Exception as error:
            return response.InternalServerError(f"Get NFT Transaction {id} Error: {error}")

        if not nft_txn:
            return response.NotFound(f"NFT Transaction {id} Not Found")
        return response.OK("Successful", nft_txn.as_dict())

    @response.wrap_response
    def put(self, id):
        try:
            nft_txn = NFTTxn.query.get(id)
        except Exception as error:
            return response.InternalServerError(f"Get NFT Transaction {id} Error: {error}")
        if not nft_txn:
            return response.NotFound(f"NFT Transaction {id} Not Found")

        data = request.get_json(force=True)  # type: ignore
        if not data:
            return response.BadRequest("Required Data Missing")

        try:
            nft_txn_dict = nft_txn.as_dict()
            for key, value in data.items():
                if key in nft_txn_dict:
                    setattr(nft_txn, key, value)
            nft_txn.update()
        except Exception as error:
            return response.InternalServerError(
                f"NFT Transaction {id} Update Failed, Error: {error}"
            )
        return response.OK(f"NFT Transaction {id} Update Success", None)
