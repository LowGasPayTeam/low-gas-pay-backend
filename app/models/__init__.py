# -*- coding=utf-8 -*-

import json
import decimal
import warnings
import time
from datetime import datetime
from sqlalchemy import text

from ExtendRegister.db_register import db


DELETED = 1
UNDELETED = 0


class BaseModel(db.Model):

    hidden_fields = []  # 不需要返回的字段与值
    __abstract__ = True
    # id = db.Column(
    #     BIGINT(20, unsigned=True), primary_key=True, autoincrement=True, comment="id"
    # )
    # created_at = db.Column(
    #     db.DateTime, default=int(time.time()), comment="创建时间(时间戳)"
    # )
    # updated_at = db.Column(
    #     db.DateTime, onupdate=int(time.time()), comment="更新时间(时间戳)"
    # )

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    deleted = db.Column(db.Integer, nullable=False, default=UNDELETED)

    def __getitem__(self, item):
        return getattr(self, item)

    def get_columns(self):
        """
        返回所有字段对象
        :return:
        """
        return self.__table__.columns

    def get_fields(self):
        """
        返回所有字段
        :return:
        """
        return self.__dict__

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_json(self, hidden_fields=None):
        """
        Json序列化
        :param hidden_fields: 覆盖类属性 hidden_fields
        :return:
        """

        hf = (
            hidden_fields
            if hidden_fields and isinstance(hidden_fields, list)
            else self.hidden_fields
        )

        model_json = {}

        for column in self.get_fields():
            if column not in hf:  # 不需要返回的字段与值
                if hasattr(self, column):
                    field = getattr(self, column)
                    if isinstance(field, decimal.Decimal):  # Decimal -> float
                        field = round(float(field), 2)
                    elif isinstance(field, datetime):  # datetime -> str
                        field = str(field)
                    model_json[column] = field

        del model_json["_sa_instance_state"]

        return model_json

    def save(self):
        """
        新增
        :return:
        """
        try:
            db.session.add(self)
            db.session.commit()
        except BaseException as e:
            db.session.rollback()
            raise TypeError("save error {}".format(str(e)))

    @staticmethod
    def save_all(model_list):
        """
        批量新增
        :param model_list:
        :return:
        """
        try:
            db.session.add_all(model_list)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise TypeError("save_all error {}".format(str(e)))

    def delete(self):
        """
        逻辑删除
        :return:
        """
        try:
            self.deleted = DELETED
            db.session.commit()
        except BaseException as e:
            db.session.rollback()
            raise TypeError("delete error {}".format(str(e)))

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            raise TypeError("update error {}".format(str(e)))
