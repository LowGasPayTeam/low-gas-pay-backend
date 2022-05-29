# Transaction数据结构设计

token order 状态
```json
{
    "orderId": "orderid",
    "orderStatus": "Created",
    "orderType": "1to1 or ntom", // 1to1 或者1ton 或者ntom
    "orderGasType": "type1 | type2",
    "orderExecId": "order exec id",
    "orderExecStatus": "order exec status",
    "orderCreatedAt": "2022-05-56:00:00:00",
    "orderUpdatedAt": "2022-05-56:00:00:00",
    "transaction": [{
        "from": "0x123",
        "to": "0xabc",
        "contract": "0xqwerqwerwr",
        "amount": "100.10000", // 使用string表示float
        "gas_used": "0.1",
        "gas_paid_status": "",
        "gas_paid_amount": "",
        "status": ""
    },{
        "from": "0x123",
        "to": "0xxyz",
        "contract": "0xqwerqwerwr",
        "amount": "100.10000", // 使用string表示float
        "gas_used": "0.1",
        "gas_paid_status": "",
        "gas_paid_amount": "",
        "status": ""
    },{
        "from": "0xqwe",
        "to": "0xabc",
        "contract": "0xqwerqwerwr",
        "amount": "100.10000", // 使用string表示float
        "gas_used": "0.1",
        "gas_paid_status": "",
        "gas_paid_amount": "",
        "status": ""
    },{
        "from": "0xabc",
        "to": "0xxyz",
        "contract": "0xqwerqwerwr",
        "amount": "100.10000", // 使用string表示float
        "gas_used": "0.1",
        "gas_paid_status": "",
        "gas_paid_amount": "",
        "status": ""
    }]
}
```
