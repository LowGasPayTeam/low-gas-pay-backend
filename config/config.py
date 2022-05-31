# -*- coding=utf-8 -*-

import os
import configparser
from datetime import timedelta

PROJECT_NAME = "low-gas-pay-backend"


def get_config():
    """获取配置文件"""
    conf = configparser.ConfigParser()
    flask_env = str(os.environ.get("FLASK_ENV"))
    base_path = os.getcwd().split(PROJECT_NAME)[0] + "{}/config/".format(PROJECT_NAME)
    if flask_env.upper() == "DEV":
        conf.read(os.path.join(base_path, "dev.ini"))
    else:
        conf.read(os.path.join(base_path, "prd.ini"))

    return conf


class BaseConfig:
    """配置基类"""

    SECRET_KEY = "ShaHeTop-Almighty-ares"  # session加密
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)  # 设置session过期时间
    DEBUG = True
    RUN_HOST = "0.0.0.0"
    RUN_PORT = 9999


class NewConfig(BaseConfig):
    """区分配置文件"""

    conf = get_config()  # 根据环境变量获取对应的配置文件

    # base
    SECRET_KEY = conf.get("base", "SECRET_KEY")  # session加密
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)  # 设置session过期时间
    DEBUG = conf.getboolean("base", "DEBUG")
    RUN_HOST = conf.get("base", "RUN_HOST")
    RUN_PORT = conf.getint("base", "RUN_PORT")

    # mysql
    MYSQL_USERNAME = conf.get("mysql", "USERNAME")
    MYSQL_PASSWORD = conf.get("mysql", "PASSWORD")
    MYSQL_HOSTNAME = conf.get("mysql", "HOSTNAME")
    MYSQL_PORT = conf.getint("mysql", "PORT")
    MYSQL_DATABASE = conf.get("mysql", "DATABASE")
    DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(
        MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOSTNAME, MYSQL_PORT, MYSQL_DATABASE
    )
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = True

if __name__ == '__main__':
    conf = NewConfig()
    print(conf.DB_URI)
