# -*- coding=utf-8 -*-

from app.models import BaseModel, db

# from ExtendRegister.db_register import db


class TokenOrder(BaseModel):
    __tablename__ = "token_order"
    wallet_address = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Integer, nullable=False)
