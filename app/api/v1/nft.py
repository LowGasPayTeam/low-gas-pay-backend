# coding=utf-8
# pyright: reportUndefinedVariable=false, reportGeneralTypeIssues=false

# import logging
from datetime import datetime

from flask import current_app, request
from flask_restful import Resource, reqparse

from app.models.nft_order import NFTOrder
from app.models.nft_transaction import NFTTxn
from common import response
from common.validator import validator

ORDER_CREATED = "Created"
ORDER_CANCELED = "Canceled"

POST_SCHEMA = {
    "type": "object",
    "properties": {
        "order_gas_type": {"type": "string"},
        "order_create_addr": {"type": "string", "pattern": "^0x[a-fA-F0-9]{40}$"},
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
                    "token_name": {"type": "string"},
                    "collection_name": {"type": "string"},
                    "token_contract": {
                        "type": "string",
                        "pattern": "^0x[a-fA-F0-9]{40}$",
                    },
                    "from_addr": {"type": "string", "pattern": "^0x[a-fA-F0-9]{40}$"},
                    "to_addr": {"type": "string", "pattern": "^0x[a-fA-F0-9]{40}$"},
                    "trans_status": {"type": "string"},
                    "trans_gas_paid_amount": {"type": "string"},
                    "trans_gas_paid_status": {"type": "string"},
                    "trans_gas_used": {"type": "string"},
                },
                "required": [
                    "token_id",
                    "token_name",
                    "collection_name",
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

UPDATE_SCHEMA = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "enum": ["cancel_order"]
        },
        "data": {
            "type": "object",
        }
    },
    "required": ["action"]
}


class NFTListApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "page", type=int, required=False, location="args")
        self.parser.add_argument(
            "size", type=int, required=False, location="args")
        self.parser.add_argument(
            "address", type=str, required=False, location="args")
        self.parser.add_argument(
            "status", type=str, required=False, location="args")

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
                current_app.logger.error(f"Get NFT Order Error: {e}")
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
            current_app.logger.info(f"Get NFT Order By Address: {address}")
            return response.OK(None, resp)
        else:
            try:
                items = NFTOrder.query.filter_by(**filters).all()
                total = len(items)
            except Exception as e:
                current_app.logger.error(f"Get NFT Order Error: {e}")
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
            return response.OK(None, resp)

    @response.wrap_response
    @validator(POST_SCHEMA)
    def post(self):
        data = request.get_json(force=True)  # type: ignore
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
                token_name=t.get("token_name"),
                collection_name=t.get("collection_name"),
            )
            nft_order.transactions.append(txn)

        try:
            nft_order.save()
        except Exception as error:
            current_app.logger.error(f"Create NFT Order Error: {error}")
            return response.InternalServerError("Create NFT Order Failed")

        try:
            saved_nft_order = NFTOrder.query.get(nft_order.order_id)
        except Exception as error:
            current_app.logger.error(
                f"Get After Create NFT Order Error: {error}")
            return response.InternalServerError(
                f"Get NFT Order {nft_order.order_id} Error: {error}"
            )

        if not saved_nft_order:
            current_app.logger.error(
                f"NFT Order {nft_order.order_id} Not Found")
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
            current_app.logger.error(f"Get NFT Order {id} Error: {error}")
            return response.InternalServerError(f"Get NFT Order {id} Error: {error}")

        if not nft_order:
            current_app.logger.error(f"NFT Order {id} Not Found")
            return response.NotFound(f"NFT Order {id} Not Found")

        nft_order_dict = nft_order.as_dict()
        trans_list = []
        for item in nft_order.transactions:
            trans_list.append(item.as_dict())
        nft_order_dict["transactions"] = trans_list
        return response.OK("Successful", nft_order_dict)

    @response.wrap_response
    def put(self, id):
        request_data = request.get_json(force=True)  # type: ignore
        action = request_data.get("action")
        data = request_data.get("data")
        return self.dispatch(id, action, data)

    def dispatch(self, id, action, data):
        try:
            nft_order = NFTOrder.query.get(id)
        except Exception as error:
            current_app.logger.error(f"Get NFT Order {id} Error: {error}")
            return response.InternalServerError(f"Get NFT Order {id} Error: {error}")
        if not nft_order:
            current_app.logger.error(f"NFT Order {id} Not Found")
            return response.NotFound(f"NFT Order {id} Not Found")

        fn = getattr(self, action)
        if not fn:
            return response.NotFound(f"Action {action} Not Found")

        return fn(nft_order, data)

    @validator(UPDATE_SCHEMA)
    def cancel_order(self, nft_order, *args, **kwargs):
        try:
            nft_order_dict = nft_order.as_dict()
            if "order_status" in nft_order_dict:
                setattr(nft_order, "order_status", ORDER_CANCELED)
            else:
                current_app.logger.warn("Undefined Feild")
                return response.Forbidden("Undefined Feild")
            nft_order.update()
        except Exception as error:
            current_app.logger.error(
                f"Token Order {id} Update Failed, Error: {error}")
            return response.InternalServerError(
                f"Token Order {nft_order.order_id} Update Failed, Error: {error}"
            )
        return response.OK(f"Token Order {nft_order.order_id} Update Success", None)

    @response.wrap_response
    def delete(self, id):
        try:
            nft_order = NFTOrder.query.get(id)
        except Exception as error:
            current_app.logger.error(f"Get NFT Order {id} Error: {error}")
            return response.InternalServerError(f"Get NFT Order {id} Error: {error}")
        if not nft_order:
            current_app.logger.error(f"NFT Order {id} Not Found")
            return response.NotFound(f"NFT Order {id} Not Found")

        try:
            nft_order.delete()
        except Exception as error:
            current_app.logger.error(f"Delete NFT Order {id} Error: {error}")
            return response.InternalServerError(f"Delete NFT Order {id} Error: {error}")

        return response.OK(f"NFT Order {id} Deleted", None)
