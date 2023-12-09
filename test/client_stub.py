class ClientStub:

    def create_order(self, symbol, side, type, quantity):
        return {
            "symbol": "BTCUSDT",
            "orderId": 19744496177,
            "orderListId": -1,
            "clientOrderId": "Y9Retn0xMZW0u8R9EzGaAl",
            "transactTime": 1678380403996,
            "price": "0.00000000",
            "origQty": "0.00088000",
            "executedQty": "0.00088000",
            "cummulativeQuoteQty": "18.89549200",
            "status": "FILLED",
            "timeInForce": "GTC",
            "type": "MARKET",
            "side": "BUY",
            "workingTime": 1678380403996,
            "fills": [
                {
                    "price": "21472.15000000",
                    "qty": "0.00088000",
                    "commission": "0.00000000",
                    "commissionAsset": "BNB",
                    "tradeId": 2903179679
                }
            ],
            "selfTradePreventionMode": "NONE"
        }

    def create_oco_order(self, symbol, side, quantity, price, stopPrice, stopLimitPrice, stopLimitTimeInForce):
        return {
            "orderListId": 84639529,
            "contingencyType": "OCO",
            "listStatusType": "EXEC_STARTED",
            "listOrderStatus": "EXECUTING",
            "listClientOrderId": "bylhWBSdMpHvD8yPeacLg4",
            "transactionTime": 1678383782170,
            "symbol": "BTCUSDT",
            "orders": [
                {
                    "symbol": "BTCUSDT",
                    "orderId": 19747264210,
                    "clientOrderId": "jZnI57Ch8SnDHeIXOpVVNP"
                },
                {
                    "symbol": "BTCUSDT",
                    "orderId": 19747264211,
                    "clientOrderId": "KNt6NgNLFrdlBAWaiAB94M"
                }
            ],
            "orderReports": [
                {
                    "symbol": "BTCUSDT",
                    "orderId": 19747264210,
                    "orderListId": 84639529,
                    "clientOrderId": "jZnI57Ch8SnDHeIXOpVVNP",
                    "transactTime": 1678383782170,
                    "price": "21444.63000000",
                    "origQty": "0.00088000",
                    "executedQty": "0.00000000",
                    "cummulativeQuoteQty": "0.00000000",
                    "status": "NEW",
                    "timeInForce": "GTC",
                    "type": "STOP_LOSS_LIMIT",
                    "side": "SELL",
                    "stopPrice": "21443.63000000",
                    "workingTime": -1,
                    "selfTradePreventionMode": "NONE"
                },
                {
                    "symbol": "BTCUSDT",
                    "orderId": 19747264211,
                    "orderListId": 84639529,
                    "clientOrderId": "KNt6NgNLFrdlBAWaiAB94M",
                    "transactTime": 1678383782170,
                    "price": "21508.03000000",
                    "origQty": "0.00088000",
                    "executedQty": "0.00000000",
                    "cummulativeQuoteQty": "0.00000000",
                    "status": "NEW",
                    "timeInForce": "GTC",
                    "type": "LIMIT_MAKER",
                    "side": "SELL",
                    "workingTime": 1678383782170,
                    "selfTradePreventionMode": "NONE"
                }
            ]
        }

    def get_order(self, symbol, orderId):
        return {
            "symbol": "BTCUSDT",
            "orderId": 19747264211,
            "orderListId": 84639529,
            "clientOrderId": "KNt6NgNLFrdlBAWaiAB94M",
            "price": "21508.03000000",
            "origQty": "0.00088000",
            "executedQty": "0.00000000",
            "cummulativeQuoteQty": "0.00000000",
            "status": "FILLED",
            "timeInForce": "GTC",
            "type": "LIMIT_MAKER",
            "side": "SELL",
            "stopPrice": "0.00000000",
            "icebergQty": "0.00000000",
            "time": 1678383782170,
            "updateTime": 1678383866396,
            "isWorking": True,
            "workingTime": 1678383782170,
            "origQuoteOrderQty": "0.00000000",
            "selfTradePreventionMode": "NONE"
        }
