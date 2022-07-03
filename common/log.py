#coding=utf-8

import logging
import os

def get_logger():
    logger_name = "gunicorn.info"
    if os.environ.get("FLASK_ENV") == "DEV":
        logger_name = "gunicorn.debug"

    return logging.getLogger(logger_name)
