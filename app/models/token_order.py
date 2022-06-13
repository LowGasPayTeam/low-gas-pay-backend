# -*- coding=utf-8 -*-

import json
# from dataclasses import dataclass
from app.models import BaseModel, db
from sqlalchemy.dialects.mysql import BIGINT

# from ExtendRegister.db_register import db


class TokenOrder(BaseModel):
    __tablename__ = "token_order"
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="id")
    order_status = db.Column(db.String(10), nullable=False)
    order_gas_type = db.Column(db.String(10), nullable=False)
    order_exec_id = db.Column(db.String(255), nullable=True)
    order_exec_status = db.Column(db.String(10), nullable=True)
    order_create_addr = db.Column(db.String(255), nullable=False)
    trans_gas_fee_max = db.Column(db.String(63), nullable=True)
    trans_gas_fee_limit = db.Column(db.String(63), nullable=True)
    trans_begin_time = db.Column(db.TIMESTAMP(True), nullable=True)
    trans_end_time = db.Column(db.TIMESTAMP(True), nullable=True)
    transactions = db.relationship("TokenTxn", backref="TokenOrder", lazy=True)


# class Transaction(object):
#     def __init__(self, from_addr, to_addr, token_contract, token_amount):
#         self.from_addr = from_addr
#         self.to_addr = to_addr
#         self.token_contract = token_contract
#         self.token_amount = token_amount
#         self.trans_date = None
#         self.trans_status = None
#         self.trans_gas_used = None
#         self.trans_gas_paid_amount = None
#         self.trans_txn = None
#         self.trans_txn_id = None
#         self.trans_gas_txn_ratio = None
#
#     def to_json(self):
#         return json.dumps(self.__dict__)
