# -*- coding=utf-8 -*-


from flask import Blueprint


nft_order_bp = Blueprint("nft_order_bp", __name__)


@nft_order_bp.route("/", methods=["GET"])
def get_orders():
    pass

@nft_order_bp.route("/<order_id>", methods=["GET"])
def get_order_by_id(order_id: str):
    print(order_id)
    pass
