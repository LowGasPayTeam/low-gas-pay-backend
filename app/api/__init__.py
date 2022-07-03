# coding=utf-8

from flask import Blueprint
from flask_restful import Api

from .v1.token import TokenListApi, TokenApi
from .v1.txn import TxnApi
from .v1.nft import NFTListApi, NFTApi
from .v1.nft_txn import NFTTxnApi
from .v1.gas import GasApi

rest_api_bp = Blueprint("api", __name__)
api = Api(rest_api_bp)

api.add_resource(GasApi, "/v1/gas", endpoint="gas")

api.add_resource(TokenListApi, "/v1/tokens", endpoint="tokens")
api.add_resource(TokenApi, "/v1/tokens/<int:id>", endpoint="token")
api.add_resource(TxnApi, "/v1/txn/<int:id>", endpoint="txn")

api.add_resource(NFTListApi, "/v1/nfts", endpoint="nfts")
api.add_resource(NFTApi, "/v1/nfts/<int:id>", endpoint="nft")
api.add_resource(NFTTxnApi, "/v1/nft_txn/<int:id>", endpoint="nft_txn")
