# -*- coding=utf-8 -*-

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def register_db(app):
    db.init_app(app)
