# -*- coding=utf-8 -*-
import logging
from create_app import create_app

app = create_app()

def main():
    host = app.config["RUN_HOST"]
    port = app.config["RUN_PORT"]
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
