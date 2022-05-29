# low-gas-pay-backend
low gas pay backend

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
