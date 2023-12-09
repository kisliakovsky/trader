"""This module contains a client with specific methods over basic Binance client's methods"""
import time
from abc import ABC, abstractmethod
from logging import Logger
from typing import Any
from _decimal import Decimal

from bot import binance_client


class Order(ABC):
    def __init__(self, id: int):
        self.__id = id

    def id(self) -> int:
        return self.__id

    @abstractmethod
    def get_status(self, client) -> str:
        pass


class LimitMakerOrder(Order):
    def __init__(self, id: int):
        super().__init__(id)

    def get_status(self, client) -> str:
        return client.poll_terminal_order_status(self.id())

    def __eq__(self, other):
        if isinstance(other, LimitMakerOrder):
            return self.id() == other.id()
        return False

    def __str__(self) -> str:
        return f"Limit maker order {self.id()}"


class MarketOrder(Order):
    def __init__(self, id: int, status: str, price: str):
        self.__status = status
        self.__price = price
        super().__init__(id)

    def price(self) -> str:
        return self.__price

    def get_status(self, client) -> str:
        return self.__status

    def __eq__(self, other):
        if isinstance(other, MarketOrder):
            return self.id() == other.id() and self.__status == self.__status and self.__price == self.__price
        return False

    def __str__(self) -> str:
        return f"Marker order {self.id()}, price {self.__price}"


class TradeClient(ABC):

    @abstractmethod
    def buy_market_order(self, quantity: float) -> MarketOrder:
        pass

    @abstractmethod
    def sell_market_order(self, quantity: float) -> MarketOrder:
        pass

    @abstractmethod
    def sell_oco_order(self, quantity: float, market_price: str) -> LimitMakerOrder:
        pass

    @abstractmethod
    def buy_oco_order(self, quantity: float, market_price: str) -> LimitMakerOrder:
        pass

    @abstractmethod
    def poll_terminal_order_status(self, order_id: int) -> str:
        pass


class LoggingTradeClient(TradeClient):
    def __init__(self, trade_client: TradeClient, logger: Logger):
        self.__trade_client = trade_client
        self.__logger = logger

    def buy_market_order(self, quantity: float) -> MarketOrder:
        order = self.__trade_client.buy_market_order(quantity)
        self.__logger.debug(str(order))
        return order

    def sell_market_order(self, quantity: float) -> MarketOrder:
        order = self.__trade_client.sell_market_order(quantity)
        self.__logger.debug(str(order))
        return order

    def sell_oco_order(self, quantity: float, market_price: str) -> Order:
        order = self.__trade_client.sell_oco_order(quantity, market_price)
        self.__logger.debug(str(order))
        return order

    def buy_oco_order(self, quantity: float, market_price: str) -> Order:
        order_id = self.__trade_client.buy_oco_order(quantity, market_price)
        self.__logger.debug(str(order_id))
        return order_id

    def poll_terminal_order_status(self, order_id: int) -> str:
        self.__logger.debug('Start polling order %s status', order_id)
        status = self.__trade_client.poll_terminal_order_status(order_id)
        self.__logger.debug('The order %s status: %s', order_id, status)
        return status


class RecoveringTradeClient(TradeClient):
    def __init__(self, client: TradeClient):
        self.__client = client

    def buy_market_order(self, quantity: float) -> MarketOrder:
        return self.__client.buy_market_order(quantity)

    def sell_market_order(self, quantity: float) -> MarketOrder:
        return self.__client.sell_market_order(quantity)

    def sell_oco_order(self, quantity: float, market_price: str) -> Order:
        try:
            order = self.__client.sell_oco_order(quantity, market_price)
        except binance_client.PriceOcoOrderException:
            order = self.__client.sell_market_order(quantity)
        return order

    def buy_oco_order(self, quantity: float, market_price: str) -> Order:
        try:
            order = self.__client.buy_oco_order(quantity, market_price)
        except binance_client.PriceOcoOrderException:
            order = self.__client.buy_market_order(quantity)
        return order

    def poll_terminal_order_status(self, order_id: int) -> str:
        return self.__client.poll_terminal_order_status(order_id)


class BasicTradeClient(TradeClient):
    def __init__(
            self,
            client,
            sell_raise_coefficient: Decimal,
            sell_decrease_coefficient: Decimal,
            buy_raise_coefficient: Decimal,
            buy_decrease_coefficient: Decimal,
    ):
        self.__client = client
        self.__sell_raise_coefficient = sell_raise_coefficient
        self.__sell_decrease_coefficient = sell_decrease_coefficient
        self.__buy_raise_coefficient = buy_raise_coefficient
        self.__buy_decrease_coefficient = buy_decrease_coefficient
        self.__decimal_digits = 2
        self.__symbol = 'BTCUSDT'

    def buy_market_order(self, quantity: float) -> MarketOrder:
        return self.__market_order(quantity, 'BUY')

    def sell_market_order(self, quantity: float) -> MarketOrder:
        return self.__market_order(quantity, 'SELL')

    def __market_order(self, quantity: float, side: str) -> MarketOrder:
        request = {
            'symbol': self.__symbol,
            'side': side,
            'type': 'MARKET',
            'quantity': quantity
        }
        response = self.__client.create_order(**request)
        status = response['status']
        fills = response['fills']
        if status == 'FILLED':
            if fills:
                return MarketOrder(response['orderId'], status, fills[0]['price'])
            raise ValueError(f"Price is undefined: {response}")
        raise ValueError(f"Unexpected order status: {status}")

    def sell_oco_order(self, quantity: float, market_price: str) -> Order:
        limit_price = str(round(Decimal(market_price) * self.__sell_raise_coefficient, self.__decimal_digits))
        stop_price = str(round(Decimal(market_price) * self.__sell_decrease_coefficient, self.__decimal_digits))
        return self.__oco_order(quantity, 'SELL', limit_price, stop_price)

    def buy_oco_order(self, quantity: float, market_price: str) -> Order:
        limit_price = str(round(Decimal(market_price) * self.__buy_decrease_coefficient, self.__decimal_digits))
        stop_price = str(round(Decimal(market_price) * self.__buy_raise_coefficient, self.__decimal_digits))
        return self.__oco_order(quantity, 'BUY', limit_price, stop_price)

    def __oco_order(self, quantity: float, side: str, limit_price: str, stop_price: str) -> LimitMakerOrder:
        request = {
            'symbol': self.__symbol,
            'side': side,
            'quantity': quantity,
            'price': limit_price,
            'stopPrice': stop_price,
            'stopLimitPrice': stop_price,
            'stopLimitTimeInForce': 'GTC'
        }
        response = self.__client.create_oco_order(**request)
        return self.__limit_maker_order(response)

    def __limit_maker_order(self, oco_order: dict[str, Any]) -> LimitMakerOrder:
        oco_status = oco_order['listOrderStatus']
        if oco_status in ('EXECUTING', 'ALL_DONE'):
            reports = oco_order['orderReports']
            if len(reports) == 2:
                first_report = reports[0]
                second_report = reports[1]
                if second_report['type'] == 'LIMIT_MAKER':
                    order_id = second_report['orderId']
                elif first_report['type'] == 'LIMIT_MAKER':
                    order_id = first_report['orderId']
                else:
                    raise ValueError(f"No LIMIT MAKER order in the OCO order: {oco_order}")
                return LimitMakerOrder(order_id)
            raise ValueError(f"Order reports are undefined: {oco_order}")
        raise ValueError(f"Unexpected order status: {oco_status}")

    def poll_terminal_order_status(self, order_id: int) -> str:
        polling_counter = 1
        status = self.__get_order_status(order_id)
        while status in ('NEW', 'PARTIALLY_FILLED'):
            time.sleep(2)
            polling_counter = polling_counter + 1
            status = self.__get_order_status(order_id)
        return status

    def __get_order_status(self, order_id: int) -> str:
        response = self.__client.get_order(symbol=self.__symbol, orderId=order_id)
        return response['status']
