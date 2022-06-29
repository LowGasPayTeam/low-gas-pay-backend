# coding=utf-8
# pyright: reportUndefinedVariable=false, reportGeneralTypeIssues=false

import logging
from datetime import datetime

from flask import request
from flask_restful import Resource, reqparse

from app.models.token_order import TokenOrder
from app.models.token_transaction import TokenTxn
from common import response
from common.validator import validator

ORDER_CREATED = "Created"

POST_SCHEMA = {
    "type": "object",
    "properties": {
        "order_gas_type": {"type": "string"},
        "order_create_addr": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$",
        },
        "trans_begin_time": {"type": "string"},
        "trans_end_time": {"type": "string"},
        "trans_gas_fee_limit": {"type": "string"},
        "trans_gas_fee_max": {"type": "string"},
        "transactions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "token_amount": {"type": "string"},
                    "token_contract": {
                        "type": "string",
                        "pattern": "^0x[a-fA-F0-9]{40}$"
                    },
                    "from_addr": {
                        "type": "string",
                        "pattern": "^0x[a-fA-F0-9]{40}$"
                    },
                    "to_addr": {
                        "type": "string",
                        "pattern": "^0x[a-fA-F0-9]{40}$"
                    },
                    "trans_status": {"type": "string"},
                    "trans_gas_paid_amount": {"type": "string"},
                    "trans_gas_paid_status": {"type": "string"},
                    "trans_gas_used": {"type": "string"},
                },
                "required": [
                    "token_amount",
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


class TokenListApi(Resource):
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
                pagination = TokenOrder.query.filter_by(**filters).paginate(
                    page, per_page=size, error_out=False
                )
                total = TokenOrder.query.filter_by(**filters).count()

            except Exception as e:
                logging.error(f"Get Token Order Error: {e}")
                return response.InternalServerError(
                    f"Get Token Order From Address {address} Failed"
                )

            orders = list()
            for token_order in pagination.items:
                token_order_dict = token_order.as_dict()
                trans_list = []
                for item in token_order.transactions:
                    trans_list.append(item.as_dict())
                token_order_dict["transactions"] = trans_list
                orders.append(token_order_dict)

            resp = {"total": total, "orders": orders}
            logging.info(f"Get Token Order By {address}")
            return response.OK(None, resp)
        else:
            try:
                items = TokenOrder.query.filter_by(**filters).all()
                total = len(items)
            except Exception as e:
                logging.error(f"Get Token Order Error: {e}")
                return response.InternalServerError(
                    f"Get Token Order From Address {address} Failed"
                )

            orders = list()
            for token_order in items:
                print(token_order.transactions)
                token_order_dict = token_order.as_dict()
                trans_list = []
                for item in token_order.transactions:
                    trans_list.append(item.as_dict())
                token_order_dict["transactions"] = trans_list
                orders.append(token_order_dict)

            resp = {"total": total, "orders": orders}
            logging.info(f"Get Token Order By {address}")
            return response.OK(None, resp)

    @response.wrap_response
    @validator(POST_SCHEMA)
    def post(self):
        data = request.get_json(force=True)  # type: ignore

        order_create_addr = data.get("order_create_addr")  # type: ignore
        transactions = data.get("transactions")  # type: ignore
        trans_begin_time = datetime.strptime(
            data.get("trans_begin_time"), "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        trans_end_time = datetime.strptime(
            data.get("trans_end_time"), "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        trans_gas_fee_limit = data.get("trans_gas_fee_limit")
        trans_gas_fee_max = data.get("trans_gas_fee_max")

        token_order = TokenOrder(
            order_status=ORDER_CREATED,
            order_gas_type=data.get("order_gas_type"),  # type: ignore
            order_create_addr=order_create_addr,  # type: ignore
            trans_begin_time=trans_begin_time,
            trans_end_time=trans_end_time,
            trans_gas_fee_limit=trans_gas_fee_limit,
            trans_gas_fee_max=trans_gas_fee_max,
        )

        for t in transactions:
            txn = TokenTxn(
                from_addr=t.get("from_addr"),
                to_addr=t.get("to_addr"),
                token_contract=t.get("token_contract"),
                token_amount=t.get("token_amount"),
            )
            token_order.transactions.append(txn)

        try:
            token_order.save()
        except Exception as error:
            print(error)
            return response.InternalServerError("Create Token Order Failed")

        try:
            saved_token_order = TokenOrder.query.get(token_order.order_id)
        except Exception as error:
            return response.InternalServerError(
                f"Get Token Order {token_order.order_id} Error: {error}"
            )

        if not saved_token_order:
            return response.NotFound(f"Token Order {token_order.order_id} Not Found")

        token_order_dict = saved_token_order.as_dict()
        trans_list = []
        for item in token_order.transactions:
            trans_list.append(item.as_dict())
        token_order_dict["transactions"] = trans_list
        logging.info(f"Token Order {saved_token_order.order_id} Created")
        return response.OK("Successful", token_order_dict)


class TokenApi(Resource):
    @response.wrap_response
    def get(self, id):
        try:
            token_order = TokenOrder.query.get(id)
        except Exception as error:
            return response.InternalServerError(f"Get Token Order {id} Error: {error}")

        if not token_order:
            return response.NotFound(f"Token Order {id} Not Found")

        token_order_dict = token_order.as_dict()
        trans_list = []
        for item in token_order.transactions:
            trans_list.append(item.as_dict())
        token_order_dict["transactions"] = trans_list
        return response.OK("Successful", token_order_dict)

    @response.wrap_response
    def put(self, id):
        try:
            token_order = TokenOrder.query.get(id)
        except Exception as error:
            return response.InternalServerError(f"Get Token Order {id} Error: {error}")
        if not token_order:
            return response.NotFound(f"Token Order {id} Not Found")

        data = request.get_json(force=True)  # type: ignore
        if not data:
            return response.BadRequest("Required Data Missing")

        try:
            token_order_dict = token_order.as_dict()
            for key, value in data.items():
                if key in token_order_dict:
                    setattr(token_order, key, value)
                else:
                    logging.warn(f"Undefined Feild: {key}")
            token_order.update()
        except Exception as error:
            return response.InternalServerError(
                f"Token Order {id} Update Failed, Error: {error}"
            )
        return response.OK(f"Token Order {id} Update Success", None)

    @response.wrap_response
    def delete(self, id):
        try:
            token_order = TokenOrder.query.get(id)
        except Exception as error:
            return response.InternalServerError(f"Get Token Order {id} Error: {error}")
        if not token_order:
            return response.NotFound(f"Token Order {id} Not Found")

        try:
            token_order.delete()
        except Exception as error:
            return response.InternalServerError(
                f"Delete Token Order {id} Error: {error}"
            )

        return response.OK(f"Token Order {id} Deleted", None)
