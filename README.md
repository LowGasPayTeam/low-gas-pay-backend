# low-gas-pay-backend

low gas pay backend

## 环境准备

- [安装 Docker](https://docs.docker.com/engine/install/ubuntu/)
- 输入密码登陆 dockerhub
  ```shell
  docker login --username lowgaspay --password-stdin
  ```
- 部署 Mysql
  ```shell
  sudo docker run --name db -d -e MYSQL_ROOT_PASSWORD={ROOT_PASSWORD} -v /path/to/data:/var/lib/mysql -v /etc/localtime:/etc/localtime -p 127.0.0.1:3306:3306 mysql:5.7
  ```
- 创建数据库、用户并分配权限
  ```shell
  mysql --host=localhost --port=3306 --protocol=TCP -uroot -p{ROOT_PASSWORD}
  > create database lowgaspay;
  > CREATE USER 'lgp'@'%' IDENTIFIED WITH mysql_native_password BY '{USER_PASSWORD}';
  > GRANT ALL PRIVILEGES ON lowgaspay.* TO 'lgp'@'%';
  > flush privileges;
  ```

## 服务部署

- 创建配置目录

  ```shell
  mkdir -p /path/to/config
  ```

- 创建`prd.ini`配置文件

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

  [gas]
  API_KEY = {API_KEY}
  ORACLE_PATH = https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=
  TIMEOUT = 5
  ```

- 创建`dev.ini`配置文件

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

  [gas]
  API_KEY = {API_KEY}
  ORACLE_PATH = https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=
  TIMEOUT = 5
  ```

- 初始化数据库表

  ```json
  docker run -it --rm --link db --env FLASK_ENV=DEV --env FLASK_APP=create_app.py -v /path/to/conf:/low-gas-pay-backend/conf lowgaspay/low-gas-pay-backend:latest bash -c "flask db init && flask db migrate && flask db upgrade"
  ```

- 启动服务
  ```json
  docker run -d --name lowgaspay --env FLASK_ENV="DEV" -v /path/to/config:/low-gas-pay-backend/config -p 5000:5000 lowgaspay/low-gas-pay-backend:latest
  ```

## Token Order

### 获取所有 Token Order

- URL: `/api/v1/tokens?page={page number}&size=${page size}&address={wallet address}`
- METHOD: `GET`
- Response StatusCode: `200`, `400`, `500`
- Response Data:

  ```json
  {
    "code": 200,
    "data": {
      "orders": [
        {
          "created_at": "Sun, 12 Jun 2022 16:27:39 GMT",
          "deleted": 0,
          "order_create_addr": "0x123456789",
          "order_exec_id": null,
          "order_exec_status": null,
          "order_gas_type": "ntom",
          "order_id": 13,
          "order_status": "Created",
          "trans_begin_time": null,
          "trans_end_time": null,
          "trans_gas_fee_limit": null,
          "trans_gas_fee_max": null,
          "transactions": [
            {
              "created_at": "Sun, 12 Jun 2022 16:27:39 GMT",
              "deleted": 0,
              "from_addr": "0x123",
              "order_id": 13,
              "to_addr": "0xabc",
              "token_amount": "100.10000",
              "token_contract": "0xqwerqwerwr",
              "token_date": null,
              "trans_gas_paid_amount": null,
              "trans_gas_paid_status": null,
              "trans_gas_txn_rate": null,
              "trans_gas_used": null,
              "trans_id": null,
              "trans_status": "Deleted",
              "trans_txn": null,
              "txn_id": 1,
              "updated_at": "Sun, 12 Jun 2022 17:09:47 GMT"
            },
            {
              "created_at": "Sun, 12 Jun 2022 16:27:39 GMT",
              "deleted": 0,
              "from_addr": "0x123",
              "order_id": 13,
              "to_addr": "0xabc",
              "token_amount": "10.10000",
              "token_contract": "0xqwerqwerwr",
              "token_date": null,
              "trans_gas_paid_amount": null,
              "trans_gas_paid_status": null,
              "trans_gas_txn_rate": null,
              "trans_gas_used": null,
              "trans_id": null,
              "trans_status": null,
              "trans_txn": null,
              "txn_id": 2,
              "updated_at": "Sun, 12 Jun 2022 16:27:39 GMT"
            }
          ],
          "updated_at": "Sun, 12 Jun 2022 16:27:39 GMT"
        }
      ],
      "total": 1
    },
    "message": null
  }
  ```

### 创建 Token Order

- URL: `/api/v1/tokens`
- METHOD: `POST`
- Request Data:
  ```json
  {
    "order_create_addr": "0x123456789",
    "order_gas_type": "ntom",
    "transactions": [
      {
        "from_addr": "0x123",
        "to_addr": "0xabc",
        "token_amount": "100.10000",
        "token_contract": "0xqwerqwerwr",
        "trans_gas_paid_amount": "",
        "trans_gas_paid_status": "",
        "trans_gas_used": "",
        "trans_status": ""
      },
      {
        "from_addr": "0x123",
        "to_addr": "0xabc",
        "token_amount": "10.10000",
        "token_contract": "0xqwerqwerwr",
        "trans_gas_paid_amount": "",
        "trans_gas_paid_status": "",
        "trans_gas_used": "",
        "trans_status": ""
      }
    ]
  }
  ```
- Response StatusCode: `200`, `400`, `500`
- Response Data:
  ```json
  {
    "code": 200,
    "data": {
      "orders": [
        {
          "created_at": "Sun, 12 Jun 2022 16:27:39 GMT",
          "deleted": 0,
          "order_create_addr": "0x123456789",
          "order_exec_id": null,
          "order_exec_status": null,
          "order_gas_type": "ntom",
          "order_id": 13,
          "order_status": "Created",
          "trans_begin_time": null,
          "trans_end_time": null,
          "trans_gas_fee_limit": null,
          "trans_gas_fee_max": null,
          "transactions": [
            {
              "created_at": "Sun, 12 Jun 2022 16:27:39 GMT",
              "deleted": 0,
              "from_addr": "0x123",
              "order_id": 13,
              "to_addr": "0xabc",
              "token_amount": "100.10000",
              "token_contract": "0xqwerqwerwr",
              "token_date": null,
              "trans_gas_paid_amount": null,
              "trans_gas_paid_status": null,
              "trans_gas_txn_rate": null,
              "trans_gas_used": null,
              "trans_id": null,
              "trans_status": "Deleted",
              "trans_txn": null,
              "txn_id": 1,
              "updated_at": "Sun, 12 Jun 2022 17:09:47 GMT"
            },
            {
              "created_at": "Sun, 12 Jun 2022 16:27:39 GMT",
              "deleted": 0,
              "from_addr": "0x123",
              "order_id": 13,
              "to_addr": "0xabc",
              "token_amount": "10.10000",
              "token_contract": "0xqwerqwerwr",
              "token_date": null,
              "trans_gas_paid_amount": null,
              "trans_gas_paid_status": null,
              "trans_gas_txn_rate": null,
              "trans_gas_used": null,
              "trans_id": null,
              "trans_status": null,
              "trans_txn": null,
              "txn_id": 2,
              "updated_at": "Sun, 12 Jun 2022 16:27:39 GMT"
            }
          ],
          "updated_at": "Sun, 12 Jun 2022 16:27:39 GMT"
        }
      ],
      "total": 1
    },
    "message": null
  }
  ```

### 获取单个 Token Order

- URL: `/api/v1/tokens/{token order id}`
- METHOD: `GET`
- Response StatusCode: `200`, `400`, `500`
- Response Data:

  ```json
  {
    "code": 200,
    "data": {
      "orders": [
        {
          "created_at": "Sun, 12 Jun 2022 16:27:39 GMT",
          "deleted": 0,
          "order_create_addr": "0x123456789",
          "order_exec_id": null,
          "order_exec_status": null,
          "order_gas_type": "ntom",
          "order_id": 13,
          "order_status": "Created",
          "trans_begin_time": null,
          "trans_end_time": null,
          "trans_gas_fee_limit": null,
          "trans_gas_fee_max": null,
          "transactions": [
            {
              "created_at": "Sun, 12 Jun 2022 16:27:39 GMT",
              "deleted": 0,
              "from_addr": "0x123",
              "order_id": 13,
              "to_addr": "0xabc",
              "token_amount": "100.10000",
              "token_contract": "0xqwerqwerwr",
              "token_date": null,
              "trans_gas_paid_amount": null,
              "trans_gas_paid_status": null,
              "trans_gas_txn_rate": null,
              "trans_gas_used": null,
              "trans_id": null,
              "trans_status": "Deleted",
              "trans_txn": null,
              "txn_id": 1,
              "updated_at": "Sun, 12 Jun 2022 17:09:47 GMT"
            },
            {
              "created_at": "Sun, 12 Jun 2022 16:27:39 GMT",
              "deleted": 0,
              "from_addr": "0x123",
              "order_id": 13,
              "to_addr": "0xabc",
              "token_amount": "10.10000",
              "token_contract": "0xqwerqwerwr",
              "token_date": null,
              "trans_gas_paid_amount": null,
              "trans_gas_paid_status": null,
              "trans_gas_txn_rate": null,
              "trans_gas_used": null,
              "trans_id": null,
              "trans_status": null,
              "trans_txn": null,
              "txn_id": 2,
              "updated_at": "Sun, 12 Jun 2022 16:27:39 GMT"
            }
          ],
          "updated_at": "Sun, 12 Jun 2022 16:27:39 GMT"
        }
      ],
      "total": 1
    },
    "message": null
  }
  ```

### 删除 Token Order

- URL: `/api/v1/tokens/{token order id}`
- METHOD: `DELETE`
- Response StatusCode: `200`, `400`, `500`
- Response Data:
  ```json
  {
    "code": 200,
    "data": null,
    "message": "Token Order 10 Deleted"
  }
  ```

### 修改 Token Order

- URL: `/api/v1/tokens/{token order id}`
- METHOD: `PUT`
- Request Data:
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
    "trans_gas_fee_max": null
  }
  ```
- Response StatusCode: `200`, `400`, `500`
- Response Data:
  ```json
  {
    "code": 200,
    "data": null,
    "message": "Token Order 10 Update Success"
  }
  ```

## Gas Price

### 获取 Gas Price

- URL: `/api/v1/gas`
- METHOD: `GET`
- Response StatusCode: `200`, `400`, `500`
- Response Data:
  ```json
  {
    "code": 200,
    "data": {
      "high": "73",
      "low": "71",
      "mid": "72",
      "suggest": "70.961895154"
    },
    "message": "Success"
  }
  ```

## Token Transaction

### 获取 txn

- URL: `/api/v1/txn/{txn_id}`
- METHOD: `GET`
- Response StatusCode: `200`, `400`, `500`
- Response Data:
  ```json
  {
    "code": 200,
    "data": {
      "created_at": "Sun, 12 Jun 2022 16:27:39 GMT",
      "deleted": 0,
      "from_addr": "0x123",
      "order_id": 13,
      "to_addr": "0xabc",
      "token_amount": "100.10000",
      "token_contract": "0xqwerqwerwr",
      "token_date": null,
      "trans_gas_paid_amount": null,
      "trans_gas_paid_status": null,
      "trans_gas_txn_rate": null,
      "trans_gas_used": null,
      "trans_id": null,
      "trans_status": "Deleted",
      "trans_txn": null,
      "txn_id": 1,
      "updated_at": "Sun, 12 Jun 2022 17:09:47 GMT"
    },
    "message": "Successful"
  }
  ```

### 修改txn

- URL: `/api/v1/txn/{txn_id}`
- METHOD: `PUt`
- Request
    ```json
    {
      "trans_status": "Succeed"
    }
    ```

- Response StatusCode: `200`, `400`, `500`
- Response Data:
  ```json
  {
    "code": 200,
    "data": {
      "created_at": "Sun, 12 Jun 2022 16:27:39 GMT",
      "deleted": 0,
      "from_addr": "0x123",
      "order_id": 13,
      "to_addr": "0xabc",
      "token_amount": "100.10000",
      "token_contract": "0xqwerqwerwr",
      "token_date": null,
      "trans_gas_paid_amount": null,
      "trans_gas_paid_status": null,
      "trans_gas_txn_rate": null,
      "trans_gas_used": null,
      "trans_id": null,
      "trans_status": "Succeed",
      "trans_txn": null,
      "txn_id": 1,
      "updated_at": "Sun, 12 Jun 2022 17:09:47 GMT"
    },
    "message": "Successful"
  }
  ```
