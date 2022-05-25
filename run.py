# -*- coding=utf-8 -*-

from create_app import create_app

def main():
    app = create_app()

    host = app.config["RUN_HOST"]
    port = app.config["RUN_PORT"]

    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
