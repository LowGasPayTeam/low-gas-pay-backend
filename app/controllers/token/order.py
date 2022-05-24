# -*- coding=utf-8 -*-

from flask import Blueprint


token_order_bp = Blueprint("token_order_bp", __name__)


@token_order_bp.route("/", methods=["GET"])
def get_orders():
    pass


@token_order_bp.route("/<order_id>", methods=["GET"])
def get_order_by_id(order_id: str):
    print(order_id)
