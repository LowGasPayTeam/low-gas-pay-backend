# -*- coding=utf-8 -*-

from app.models import BaseModel, db


class NFTTxn(BaseModel):
    __tablename__ = "nft_txn"
    txn_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="id")
    order_id = db.Column(
        db.Integer, db.ForeignKey("nft_order.order_id"), nullable=False
    )
    from_addr = db.Column(db.String(255), nullable=False)
    to_addr = db.Column(db.String(255), nullable=False)
    token_contract = db.Column(db.String(255), nullable=False)
    token_id = db.Column(db.String(63), nullable=False)
    token_name = db.Column(db.String(63), nullable=False)
    collection_name = db.Column(db.String(63), nullable=False)
    token_date = db.Column(db.DateTime, nullable=True)

    trans_id = db.Column(db.String(255))
    trans_txn = db.Column(db.Text)
    trans_status = db.Column(db.String(10))
    trans_gas_used = db.Column(db.String(63))
    trans_gas_paid_amount = db.Column(db.String(63))
    trans_gas_paid_status = db.Column(db.String(63))
    trans_gas_txn_rate = db.Column(db.String(10))
