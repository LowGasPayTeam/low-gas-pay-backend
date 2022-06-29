# -*- coding=utf-8 -*-

import logging

from config.config import NewConfig


def register_config(app):
    """配置文件"""

    config = NewConfig()
    app.config.from_object(config)  # 环境配置
    #
    # log_level = "gunicorn.info"
    # if config.DEBUG:
    #     log_level = "gunicorn.debug"
    #
    # gunicorn_logger = logging.getLogger(log_level)
    # app.logger.handlers = gunicorn_logger.handlers
    # app.logger.setLevel(gunicorn_logger.level)
