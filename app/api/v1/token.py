# coding=utf-8
# pyright: reportUndefinedVariable=false, reportGeneralTypeIssues=false

import logging
# import json
from flask import request
from flask_restful import Resource, reqparse
from app.models.token_order import TokenOrder
from app.models.token_transaction import TokenTxn
from common.validator import validator
from common.response import *

ORDER_CREATED = "Created"

POST_SCHEMA = {
    "type": "object",
    "properties": {
        "order_gas_type": {"type": "string"},
        "order_gas_type": {"type": "string"},
        "transactions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "amount": {"type": "string"},
                    "contract": {"type": "string"},
                    "from": {"type": "string"},
                    "to": {"type": "string"},
                    "status": {"type": "string"},
                    "gas_paid_amount": {"type": "string"},
                    "gas_paid_status": {"type": "string"},
                    "gas_used": {"type": "string"},
                },
            },
        },
    },
}


class TokenListApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("page", type=int, required=False, location="args")
        self.parser.add_argument("size", type=int, required=False, location="args")
        self.parser.add_argument("address", type=str, required=False, location="args")
        self.parser.add_argument("status", type=str, required=False, location="args")

    @wrap_response
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
                print(e)
                return InternalServerError(
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
            return OK(None, resp)
        else:
            try:
                items = TokenOrder.query.filter_by(**filters).all()
                total = len(items)
            except Exception as e:
                print(e)
                return InternalServerError(
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
            return OK(None, resp)

    @wrap_response
    @validator(POST_SCHEMA)
    def post(self):
        data = request.get_json(force=True)  # type: ignore

        if (
            "order_gas_type" not in data
            or "order_create_addr" not in data  # type: ignore
            or "transactions" not in data  # type: ignore
        ):
            return BadRequest("Required Feild Missing")

        address = data.get("order_create_addr")  # type: ignore
        transactions = data.get("transactions") # type: ignore

        token_order = TokenOrder(
            order_status=ORDER_CREATED,
            order_gas_type=data.get("order_gas_type"),  # type: ignore
            order_create_addr=address,  # type: ignore
            # transactions=json.dumps(data.get("transactions")),  # type: ignore
        )

        for t in transactions:
            txn = TokenTxn(
                from_addr = t.get("from_addr"),
                to_addr = t.get("to_addr"),
                token_contract = t.get("token_contract"),
                token_amount=t.get("token_amount"),
            )
            token_order.transactions.append(txn)

        try:
            token_order.save()
        except Exception as error:
            print(error)
            return InternalServerError("Create Token Order Failed")

        try:
            saved_token_order = TokenOrder.query.get(id)
        except Exception as error:
            return InternalServerError(f"Get Token Order {id} Error: {error}")

        if not saved_token_order:
            return NotFound(f"Token Order {id} Not Found")

        token_order_dict = saved_token_order.as_dict()
        trans_list = []
        for item in token_order.transactions:
            trans_list.append(item.as_dict())
        token_order_dict["transactions"] = trans_list
        return OK("Successful", token_order_dict)

class TokenApi(Resource):
    @wrap_response
    def get(self, id):
        try:
            token_order = TokenOrder.query.get(id)
        except Exception as error:
            return InternalServerError(f"Get Token Order {id} Error: {error}")

        if not token_order:
            return NotFound(f"Token Order {id} Not Found")

        token_order_dict = token_order.as_dict()
        trans_list = []
        for item in token_order.transactions:
            trans_list.append(item.as_dict())
        token_order_dict["transactions"] = trans_list
        return OK("Successful", token_order_dict)

    @wrap_response
    def put(self, id):
        try:
            token_order = TokenOrder.query.get(id)
        except Exception as error:
            return InternalServerError(f"Get Token Order {id} Error: {error}")
        if not token_order:
            return NotFound(f"Token Order {id} Not Found")

        data = request.get_json(force=True)  # type: ignore
        if not data:
            return BadRequest("Required Data Missing")

        try:
            token_order_dict = token_order.as_dict()
            for key, value in data.items():
                if key in token_order_dict:
                    setattr(token_order, key, value)
            token_order.update()
        except Exception as error:
            return InternalServerError(
                f"Token Order {id} Update Failed, Error: {error}"
            )
        return OK(f"Token Order {id} Update Success", None)

    @wrap_response
    def delete(self, id):
        try:
            token_order = TokenOrder.query.get(id)
        except Exception as error:
            return InternalServerError(f"Get Token Order {id} Error: {error}")
        if not token_order:
            return NotFound(f"Token Order {id} Not Found")

        try:
            token_order.delete()
        except Exception as error:
            return InternalServerError(f"Delete Token Order {id} Error: {error}")

        return OK(f"Token Order {id} Deleted", None)
