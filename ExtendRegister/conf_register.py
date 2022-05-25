# -*- coding=utf-8 -*-

from config.config import NewConfig


def register_config(app):
    """配置文件"""

    config = NewConfig()
    app.config.from_object(config)  # 环境配置
