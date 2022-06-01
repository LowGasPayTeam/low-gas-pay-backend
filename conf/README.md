# 配置文件
* 创建配置目录
    ```shell
    mkdir -p /path/to/config
    ```

* 创建`prd.ini`配置文件
    ```ini
    [base]
    SECRET_KEY = ShaHeTop-Almighty-ares
    DEBUG = False
    RUN_HOST = 0.0.0.0
    RUN_PORT = 5000

    [mysql]
    HOSTNAME = db
    PORT = 3306
    USERNAME = lowgaspay
    PASSWORD = {USER_PASSWORD}
    DATABASE = lowgaspay
    ```

* 创建`dev.ini`配置文件
    ```ini
    [base]
    SECRET_KEY = ShaHeTop-Almighty-ares
    DEBUG = True
    RUN_HOST = 0.0.0.0
    RUN_PORT = 9999

    [mysql]
    HOSTNAME = db
    PORT = 3306
    USERNAME = lowgaspay
    PASSWORD = {USER_PASSWORD}
    DATABASE = lowgaspay
    ```
