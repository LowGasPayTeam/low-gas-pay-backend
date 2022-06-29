# -*- coding=utf-8 -*-

import logging
import os

from create_app import create_app

app = create_app()

if __name__ != "__main__":
    # log_level = "gunicorn.debug"
    # flask_env = str(os.environ.get("FLASK_ENV"))
    # if flask_env.upper() == "PRD":
    #     log_level = "gunicorn.info"

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def main():
    host = app.config["RUN_HOST"]
    port = app.config["RUN_PORT"]
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
