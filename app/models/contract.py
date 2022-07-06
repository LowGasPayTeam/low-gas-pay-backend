# coding=utf-8

from app.models import BaseModel, db


class Contract(BaseModel):
    __tablename__ = "contract"
    contract_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contract = db.Column(db.String(42), unique=True, nullable=True)
