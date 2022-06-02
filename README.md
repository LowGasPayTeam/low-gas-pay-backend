# low-gas-pay-backend
low gas pay backend

## 环境准备
* [安装Docker](https://docs.docker.com/engine/install/ubuntu/)
* 输入密码登陆dockerhub
    ```shell
    docker login --username lowgaspay --password-stdin
    ```
* 部署Mysql
    ```shell
    sudo docker run --name db -d -e MYSQL_ROOT_PASSWORD={ROOT_PASSWORD} -v /path/to/data:/var/lib/mysql -v /etc/localtime:/etc/localtime -p 127.0.0.1:3306:3306 mysql:5.7
    ```
* 创建数据库、用户并分配权限
    ```shell
    mysql --host=localhost --port=3306 --protocol=TCP -uroot -p{ROOT_PASSWORD}
    > create database lowgaspay;
    > CREATE USER 'lgp'@'%' IDENTIFIED WITH mysql_native_password BY '{USER_PASSWORD}';
    > GRANT ALL PRIVILEGES ON lowgaspay.* TO 'lgp'@'%';
    > flush privileges;
    ```

## 服务部署
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

* 初始化数据库表
    ```json
	docker run -it --rm --link db --env FLASK_ENV=DEV --env FLASK_APP=create_app.py -v /path/to/conf:/low-gas-pay-backend/conf lowgaspay/low-gas-pay-backend:latest bash -c "flask db init && flask db migrate && flask db upgrade"
    ```

* 启动服务
    ```json
	docker run -d --name lowgaspay --env FLASK_ENV="DEV" -v /path/to/config:/low-gas-pay-backend/config -p 5000:5000 lowgaspay/low-gas-pay-backend:latest
    ```

## Token Order

### 获取所有Token Order

* URL: `/api/v1/tokens?page={page number}&size=${page size}&address={wallet
  address}`
* METHOD: `GET`
* Response StatusCode: `200`, `400`, `500`
* Response Data:
    ```json
    {
        "code": 200,
        "data": [
            {
                "created_at": "2022-05-29 09:22:57",
                "deleted": 0,
                "order_create_addr": "0x123456789",
                "order_exec_id": null,
                "order_exec_status": null,
                "order_gas_type": "ntom",
                "order_id": 2,
                "order_status": "Created",
                "trans_begin_time": null,
                "trans_end_time": null,
                "trans_gas_fee_limit": null,
                "trans_gas_fee_max": null,
                "transactions": [
                    {
                        "amount": "100.10000",
                        "contract": "0xqwerqwerwr",
                        "from": "0x123",
                        "gas_paid_amount": "",
                        "gas_paid_status": "",
                        "gas_used": "0.1",
                        "status": "",
                        "to": "0xabc"
                    },
                    {
                        "amount": "100.10000",
                        "contract": "0xqwerqwerwr",
                        "from": "0x123",
                        "gas_paid_amount": "",
                        "gas_paid_status": "",
                        "gas_used": "0.1",
                        "status": "",
                        "to": "0xxyz"
                    },
                    {
                        "amount": "100.10000",
                        "contract": "0xqwerqwerwr",
                        "from": "0xqwe",
                        "gas_paid_amount": "",
                        "gas_paid_status": "",
                        "gas_used": "0.1",
                        "status": "",
                        "to": "0xabc"
                    },
                    {
                        "amount": "100.10000",
                        "contract": "0xqwerqwerwr",
                        "from": "0xabc",
                        "gas_paid_amount": "",
                        "gas_paid_status": "",
                        "gas_used": "0.1",
                        "status": "",
                        "to": "0xxyz"
                    }
                ],
                "updated_at": "2022-05-29 09:22:57"
            },
            {
                "created_at": "2022-05-29 09:25:57",
                "deleted": 0,
                "order_create_addr": "0x123456789",
                "order_exec_id": null,
                "order_exec_status": null,
                "order_gas_type": "ntom",
                "order_id": 3,
                "order_status": "Created",
                "trans_begin_time": null,
                "trans_end_time": null,
                "trans_gas_fee_limit": null,
                "trans_gas_fee_max": null,
                "transactions": [
                    {
                        "amount": "100.10000",
                        "contract": "0xqwerqwerwr",
                        "from": "0x123",
                        "gas_paid_amount": "",
                        "gas_paid_status": "",
                        "gas_used": "0.1",
                        "status": "",
                        "to": "0xabc"
                    },
                    {
                        "amount": "100.10000",
                        "contract": "0xqwerqwerwr",
                        "from": "0x123",
                        "gas_paid_amount": "",
                        "gas_paid_status": "",
                        "gas_used": "0.1",
                        "status": "",
                        "to": "0xxyz"
                    },
                    {
                        "amount": "100.10000",
                        "contract": "0xqwerqwerwr",
                        "from": "0xqwe",
                        "gas_paid_amount": "",
                        "gas_paid_status": "",
                        "gas_used": "0.1",
                        "status": "",
                        "to": "0xabc"
                    },
                    {
                        "amount": "100.10000",
                        "contract": "0xqwerqwerwr",
                        "from": "0xabc",
                        "gas_paid_amount": "",
                        "gas_paid_status": "",
                        "gas_used": "0.1",
                        "status": "",
                        "to": "0xxyz"
                    }
                ],
                "updated_at": "2022-05-29 09:25:57"
            }
        ],
        "message": null
    }
    ```

### 创建Token Order

* URL: `/api/v1/tokens`
* METHOD: `POST`
* Request Data:
    ```json
    {
      "order_create_addr": "0x123456789",
      "order_gas_type": "ntom",
      "transactions": [
        {
          "amount": "100.10000",
          "contract": "0xqwerqwerwr",
          "from": "0x123",
          "gas_paid_amount": "",
          "gas_paid_status": "",
          "gas_used": "0.1",
          "status": "",
          "to": "0xabc"
        },
        {
          "amount": "100.10000",
          "contract": "0xqwerqwerwr",
          "from": "0x123",
          "gas_paid_amount": "",
          "gas_paid_status": "",
          "gas_used": "0.1",
          "status": "",
          "to": "0xxyz"
        },
        {
          "amount": "100.10000",
          "contract": "0xqwerqwerwr",
          "from": "0xqwe",
          "gas_paid_amount": "",
          "gas_paid_status": "",
          "gas_used": "0.1",
          "status": "",
          "to": "0xabc"
        },
        {
          "amount": "100.10000",
          "contract": "0xqwerqwerwr",
          "from": "0xabc",
          "gas_paid_amount": "",
          "gas_paid_status": "",
          "gas_used": "0.1",
          "status": "",
          "to": "0xxyz"
        }
      ]
    }
    ```
* Response StatusCode: `200`, `400`, `500`
* Response Data:
    ```json
    {
        "code": 200,
        "data": {
            "created_at": "Sun, 29 May 2022 21:02:32 GMT",
            "deleted": 0,
            "order_create_addr": "0x123456789",
            "order_exec_id": null,
            "order_exec_status": null,
            "order_gas_type": "ntom",
            "order_id": 10,
            "order_status": "Created",
            "trans_begin_time": null,
            "trans_end_time": null,
            "trans_gas_fee_limit": null,
            "trans_gas_fee_max": null,
            "transactions": [
                {
                    "amount": "100.10000",
                    "contract": "0xqwerqwerwr",
                    "from": "0x123",
                    "gas_paid_amount": "",
                    "gas_paid_status": "",
                    "gas_used": "0.1",
                    "status": "",
                    "to": "0xabc"
                },
                {
                    "amount": "100.10000",
                    "contract": "0xqwerqwerwr",
                    "from": "0x123",
                    "gas_paid_amount": "",
                    "gas_paid_status": "",
                    "gas_used": "0.1",
                    "status": "",
                    "to": "0xxyz"
                },
                {
                    "amount": "100.10000",
                    "contract": "0xqwerqwerwr",
                    "from": "0xqwe",
                    "gas_paid_amount": "",
                    "gas_paid_status": "",
                    "gas_used": "0.1",
                    "status": "",
                    "to": "0xabc"
                },
                {
                    "amount": "100.10000",
                    "contract": "0xqwerqwerwr",
                    "from": "0xabc",
                    "gas_paid_amount": "",
                    "gas_paid_status": "",
                    "gas_used": "0.1",
                    "status": "",
                    "to": "0xxyz"
                }
            ],
            "updated_at": "Sun, 29 May 2022 21:02:32 GMT"
        },
        "message": "Successful"
    }
    ```

### 获取单个Token Order

* URL: `/api/v1/tokens/{token order id}`
* METHOD: `GET`
* Response StatusCode: `200`, `400`, `500`
* Response Data:
    ```json
    {
        "code": 200,
        "data": {
            "created_at": "Sun, 29 May 2022 21:02:32 GMT",
            "deleted": 0,
            "order_create_addr": "0x123456789",
            "order_exec_id": null,
            "order_exec_status": null,
            "order_gas_type": "ntom",
            "order_id": 10,
            "order_status": "Created",
            "trans_begin_time": null,
            "trans_end_time": null,
            "trans_gas_fee_limit": null,
            "trans_gas_fee_max": null,
            "transactions": [
                {
                    "amount": "100.10000",
                    "contract": "0xqwerqwerwr",
                    "from": "0x123",
                    "gas_paid_amount": "",
                    "gas_paid_status": "",
                    "gas_used": "0.1",
                    "status": "",
                    "to": "0xabc"
                },
                {
                    "amount": "100.10000",
                    "contract": "0xqwerqwerwr",
                    "from": "0x123",
                    "gas_paid_amount": "",
                    "gas_paid_status": "",
                    "gas_used": "0.1",
                    "status": "",
                    "to": "0xxyz"
                },
                {
                    "amount": "100.10000",
                    "contract": "0xqwerqwerwr",
                    "from": "0xqwe",
                    "gas_paid_amount": "",
                    "gas_paid_status": "",
                    "gas_used": "0.1",
                    "status": "",
                    "to": "0xabc"
                },
                {
                    "amount": "100.10000",
                    "contract": "0xqwerqwerwr",
                    "from": "0xabc",
                    "gas_paid_amount": "",
                    "gas_paid_status": "",
                    "gas_used": "0.1",
                    "status": "",
                    "to": "0xxyz"
                }
            ],
            "updated_at": "Sun, 29 May 2022 21:02:32 GMT"
        },
        "message": "Successful"
    }
    ```
### 删除Token Order

* URL: `/api/v1/tokens/{token order id}`
* METHOD: `DELETE`
* Response StatusCode: `200`, `400`, `500`
* Response Data:
    ```json
    {
        "code": 200,
        "data": null,
        "message": "Token Order 10 Deleted"
    }
    ```

### 修改Token Order

* URL: `/api/v1/tokens/{token order id}`
* METHOD: `PUT`
* Request Data:
    ```json
    {
      "order_create_addr": "0xabcdefg",
      "order_exec_id": null,
      "order_exec_status": null,
      "order_gas_type": "ntom",
      "order_status": "Created",
      "trans_begin_time": null,
      "trans_end_time": null,
      "trans_gas_fee_limit": null,
      "trans_gas_fee_max": null,
      "transactions": [
        {
          "amount": "100.10000",
          "contract": "0xqwerqwerwr",
          "from": "0x123",
          "gas_paid_amount": "",
          "gas_paid_status": "",
          "gas_used": "0.1",
          "status": "",
          "to": "0xabc"
        }
      ]
    }
    ```
* Response StatusCode: `200`, `400`, `500`
* Response Data:
    ```json
    {
        "code": 200,
        "data": null,
        "message": "Token Order 10 Update Success"
    }
    ```
