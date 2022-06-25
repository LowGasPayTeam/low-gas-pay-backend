# coding=utf-8
# pyright: reportUndefinedVariable=false, reportGeneralTypeIssues=false

import logging
from datetime import datetime

from flask import request
from flask_restful import Resource, reqparse

from app.models.nft_order import NFTOrder
from app.models.nft_transaction import NFTTxn
from common import response
from common.validator import validator

ORDER_CREATED = "Created"

POST_SCHEMA = {
    "type": "object",
    "properties": {
        "order_gas_type": {"type": "string"},
        "order_create_addr": {"type": "string"},
        "trans_begin_time": {"type": "string"},
        "trans_end_time": {"type": "string"},
        "trans_gas_fee_limit": {"type": "string"},
        "trans_gas_fee_max": {"type": "string"},
        "transactions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "token_id": {"type": "string"},
                    "token_contract": {"type": "string"},
                    "from_addr": {"type": "string"},
                    "to_addr": {"type": "string"},
                    "trans_status": {"type": "string"},
                    "trans_gas_paid_amount": {"type": "string"},
                    "trans_gas_paid_status": {"type": "string"},
                    "trans_gas_used": {"type": "string"},
                },
                "required": [
                    "token_id",
                    "token_contract",
                    "from_addr",
                    "to_addr",
                ],
            },
        },
    },
    "required": [
        "order_gas_type",
        "order_create_addr",
        "trans_begin_time",
        "trans_end_time",
        "trans_gas_fee_limit",
        "trans_gas_fee_max",
        "transactions",
    ],
}


class NFTListApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("page", type=int, required=False, location="args")
        self.parser.add_argument("size", type=int, required=False, location="args")
        self.parser.add_argument("address", type=str, required=False, location="args")
        self.parser.add_argument("status", type=str, required=False, location="args")

    @response.wrap_response
    def get(self):
        params = self.parser.parse_args()

        filters = {}
        filters["deleted"] = 0

        page = params.get("page", None)
        size = params.get("size", None)

        address = params.get("address", None)
        if address:
            filters["order_create_addr"] = address

        status = params.get("status", None)
        if status:
            filters["order_status"] = status

        if page and size:
            try:
                pagination = NFTOrder.query.filter_by(**filters).paginate(
                    page, per_page=size, error_out=False
                )
                total = NFTOrder.query.filter_by(**filters).count()
            except Exception as e:
                logging.error(f"Get NFT Order Error: {e}")
                return response.InternalServerError(
                    f"Get NFT Order From Address {address} Failed"
                )

            orders = list()
            for nft_order in pagination.items:
                nft_order_dict = nft_order.as_dict()
                trans_list = []
                for item in nft_order.transactions:
                    trans_list.append(item.as_dict())
                nft_order_dict["transactions"] = trans_list
                orders.append(nft_order_dict)

            resp = {"total": total, "orders": orders}
            return response.OK(None, resp)
        else:
            try:
                items = NFTOrder.query.filter_by(**filters).all()
                total = len(items)
            except Exception as e:
                logging.error(f"Get NFT Order Error: {e}")
                return response.InternalServerError(
                    f"Get NFT Order From Address {address} Failed"
                )

            orders = list()
            for nft_order in items:
                print(nft_order.transactions)
                nft_order_dict = nft_order.as_dict()
                trans_list = []
                for item in nft_order.transactions:
                    trans_list.append(item.as_dict())
                nft_order_dict["transactions"] = trans_list
                orders.append(nft_order_dict)

            resp = {"total": total, "orders": orders}
            logging.info(f"Get NFT Order By Address: {address}")
            return response.OK(None, resp)

    @response.wrap_response
    @validator(POST_SCHEMA)
    def post(self):
        data = request.get_json(force=True)  # type: ignore

        # if (
        #     "order_gas_type" not in data
        #     or "order_create_addr" not in data  # type: ignore
        #     or "transactions" not in data  # type: ignore
        #     or "trans_begin_time" not in data  # type: ignore
        #     or "trans_end_time" not in data  # ta # type: ignore
        # ):
        #     return response.BadRequest("Required Feild Missing")

        address = data.get("order_create_addr")  # type: ignore
        transactions = data.get("transactions")  # type: ignore

        trans_begin_time = datetime.strptime(
            data.get("trans_begin_time"), "%Y-%m-%dT%H:%M:%S.%fZ"
        )  # type: ignore
        trans_end_time = datetime.strptime(
            data.get("trans_end_time"), "%Y-%m-%dT%H:%M:%S.%fZ"
        )  # type: ignore
        trans_gas_fee_limit = data.get("trans_gas_fee_limit")
        trans_gas_fee_max = data.get("trans_gas_fee_max")

        nft_order = NFTOrder(
            order_status=ORDER_CREATED,
            order_gas_type=data.get("order_gas_type"),  # type: ignore
            order_create_addr=address,  # type: ignore
            trans_begin_time=trans_begin_time,
            trans_end_time=trans_end_time,
            trans_gas_fee_limit=trans_gas_fee_limit,
            trans_gas_fee_max=trans_gas_fee_max,
        )

        for t in transactions:
            txn = NFTTxn(
                from_addr=t.get("from_addr"),
                to_addr=t.get("to_addr"),
                token_contract=t.get("token_contract"),
                token_id=t.get("token_id"),
            )
            nft_order.transactions.append(txn)

        try:
            nft_order.save()
        except Exception as error:
            print(error)
            return response.InternalServerError("Create NFT Order Failed")

        try:
            saved_nft_order = NFTOrder.query.get(nft_order.order_id)
        except Exception as error:
            return response.InternalServerError(
                f"Get NFT Order {nft_order.order_id} Error: {error}"
            )

        if not saved_nft_order:
            return response.NotFound(f"NFT Order {nft_order.order_id} Not Found")

        nft_order_dict = saved_nft_order.as_dict()
        trans_list = []
        for item in nft_order.transactions:
            trans_list.append(item.as_dict())
        nft_order_dict["transactions"] = trans_list
        return response.OK("Successful", nft_order_dict)


class NFTApi(Resource):
    @response.wrap_response
    def get(self, id):
        try:
            nft_order = NFTOrder.query.get(id)
        except Exception as error:
            return response.InternalServerError(f"Get NFT Order {id} Error: {error}")

        if not nft_order:
            return response.NotFound(f"NFT Order {id} Not Found")

        nft_order_dict = nft_order.as_dict()
        trans_list = []
        for item in nft_order.transactions:
            trans_list.append(item.as_dict())
        nft_order_dict["transactions"] = trans_list
        return response.OK("Successful", nft_order_dict)

    @response.wrap_response
    def put(self, id):
        try:
            nft_order = NFTOrder.query.get(id)
        except Exception as error:
            return response.InternalServerError(f"Get NFT Order {id} Error: {error}")
        if not nft_order:
            return response.NotFound(f"NFT Order {id} Not Found")

        data = request.get_json(force=True)  # type: ignore
        if not data:
            return response.BadRequest("Required Data Missing")

        try:
            nft_order_dict = nft_order.as_dict()
            for key, value in data.items():
                if key in nft_order_dict:
                    setattr(nft_order, key, value)
                else:
                    logging.warn(f"Undefined Feild: {key}")
            nft_order.update()
        except Exception as error:
            return response.InternalServerError(
                f"NFT Order {id} Update Failed, Error: {error}"
            )
        return response.OK(f"NFT Order {id} Update Success", None)

    @response.wrap_response
    def delete(self, id):
        try:
            nft_order = NFTOrder.query.get(id)
        except Exception as error:
            return response.InternalServerError(f"Get NFT Order {id} Error: {error}")
        if not nft_order:
            return response.NotFound(f"NFT Order {id} Not Found")

        try:
            nft_order.delete()
        except Exception as error:
            return response.InternalServerError(f"Delete NFT Order {id} Error: {error}")

        return response.OK(f"NFT Order {id} Deleted", None)
