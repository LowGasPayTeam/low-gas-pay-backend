# coding=utf-8
# pyright: reportUndefinedVariable=false, reportGeneralTypeIssues=false

import json
from flask import request
from flask_restful import Resource, reqparse
from app.models.token_order import TokenOrder
from common.response import *

ORDER_CREATED = "Created"


class TokenListApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("page", type=int, required=True, location="args")
        self.parser.add_argument("size", type=int, required=True, location="args")
        self.parser.add_argument("address", type=str, required=True, location="args")

        self.post_schema = {
            "type": "object",
            "properties": {"order_gas_type": {"type": "string"}},
        }

    @wrap_response
    def get(self):
        params = self.parser.parse_args()
        page = params.get("page")
        size = params.get("size")
        address = params.get("address")
        if not address or len(address) == 0:
            return BadRequest("address required")

        try:
            pagination = TokenOrder.query.filter(
                TokenOrder.order_create_addr == address, TokenOrder.deleted == 0
            ).paginate(page, per_page=size, error_out=False)
            total = TokenOrder.query.filter(
                TokenOrder.order_create_addr == address, TokenOrder.deleted == 0
            ).count()
        except Exception as e:
            print(e)
            return InternalServerError(f"Get Token Order From Address {address} Failed")

        orders = list()
        for token_order in pagination.items:
            raw_trans = token_order.transactions
            trans = json.loads(raw_trans)
            token_order.transactions = trans
            orders.append(token_order.to_json())

        resp = {"total": total, "orders": orders}
        return OK(None, resp)

    @wrap_response
    def post(self):
        data = request.get_json(force=True)  # type: ignore

        if (
            "order_gas_type" not in data
            or "order_create_addr" not in data  # type: ignore
            or "transactions" not in data  # type: ignore
        ):
            return BadRequest("Required Feild Missing")

        address = data.get("order_create_addr")  # type: ignore
        token_order = TokenOrder(
            order_status=ORDER_CREATED,
            order_gas_type=data.get("order_gas_type"),  # type: ignore
            order_create_addr=address,  # type: ignore
            transactions=json.dumps(data.get("transactions")),  # type: ignore
        )
        try:
            token_order.save()
        except Exception as error:
            print(error)
            return InternalServerError("Create Token Order Failed")

        saved_token_order = TokenOrder.query.get(token_order.order_id)
        trans = json.loads(saved_token_order.transactions)
        saved_token_order.transactions = trans
        return Response(200, "Successful", saved_token_order.as_dict())


class TokenApi(Resource):
    @wrap_response
    def get(self, id):
        try:
            token_order = TokenOrder.query.get(id)
        except Exception as error:
            return InternalServerError(f"Get Token Order {id} Error: {error}")

        if not token_order:
            return NotFound(f"Token Order {id} Not Found")

        trans = json.loads(token_order.transactions)
        token_order.transactions = trans
        return OK("Successful", token_order.as_dict())

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

        if "transactions" in data:
            data["transactions"] = json.dumps(data["transactions"])

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
