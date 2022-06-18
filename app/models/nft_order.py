# coding=utf-8

from app.models import BaseModel, db


class NFTOrder(BaseModel):
    __tablename__ = "nft_order"
    order_id = db.Column(db.Integer, primary_key=True,
                         autoincrement=True, comment="id")
    order_status = db.Column(db.String(10), nullable=False)
    order_gas_type = db.Column(db.String(10), nullable=False)
    order_exec_id = db.Column(db.String(255), nullable=True)
    order_exec_status = db.Column(db.String(10), nullable=True)
    order_create_addr = db.Column(db.String(255), nullable=False)
    trans_gas_fee_max = db.Column(db.String(63), nullable=True)
    trans_gas_fee_limit = db.Column(db.String(63), nullable=True)
    trans_begin_time = db.Column(db.TIMESTAMP(True), nullable=True)
    trans_end_time = db.Column(db.TIMESTAMP(True), nullable=True)
    transactions = db.relationship("NFTTxn", backref="NFTOrder", lazy=True)
