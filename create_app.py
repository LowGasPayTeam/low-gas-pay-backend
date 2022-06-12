# -*- coding=utf-8 -*-

from flask import Flask
from flask_migrate import Migrate

from ExtendRegister.db_register import register_db, db
from ExtendRegister.conf_register import register_config
from ExtendRegister.bp_register import register_bp
from ExtendRegister.hook_register import register_hook
from ExtendRegister.model_register import *


def create_app():
    app = Flask(__name__)
    register_config(app)
    register_bp(app)
    register_hook(app)
    register_db(app)
    Migrate(app, db)
    return app
