from abc import ABC, abstractmethod
from itertools import cycle
from logging import Logger

from bot.counter import Counter
from bot.trade_client import TradeClient


class TradeStrategy(ABC):

    @abstractmethod
    def run(self, quantity: float) -> str:
        pass


class TradeStrategySupplier(ABC):

    @abstractmethod
    def next_strategy(self) -> TradeStrategy:
        pass


class CountingTradeStrategySupplier(TradeStrategySupplier):
    def __init__(self, supplier: TradeStrategySupplier, counter: Counter):
        self.__supplier = supplier
        self.__counter = counter

    def next_strategy(self) -> TradeStrategy:
        strategy = self.__supplier.next_strategy()
        self.__counter.inc()
        return strategy


class LoggingTradeStrategySupplier(TradeStrategySupplier):
    def __init__(self, supplier: TradeStrategySupplier, logger: Logger):
        self.__supplier = supplier
        self.__logger = logger

    def next_strategy(self) -> TradeStrategy:
        strategy = self.__supplier.next_strategy()
        self.__logger.debug("Next strategy: %s", str(strategy))
        return strategy


class CycleTradeStrategySupplier(TradeStrategySupplier):
    def __init__(self, strategies: list[TradeStrategy]):
        self.__strategies = cycle(strategies)

    def next_strategy(self) -> TradeStrategy:
        return next(self.__strategies)


class LoggingTradeStrategy(TradeStrategy):
    def __init__(self, strategy: TradeStrategy, logger: Logger):
        self.__strategy = strategy
        self.__logger = logger

    def run(self, quantity: float) -> str:
        self.__logger.debug("Run %s", self.__strategy)
        return self.__strategy.run(quantity)

    def __str__(self):
        return str(self.__strategy)


class SellStrategy(TradeStrategy):
    def __init__(self, client: TradeClient):
        self.__client = client

    def run(self, quantity: float) -> str:
        market_order = self.__client.sell_market_order(quantity)
        order = self.__client.buy_oco_order(quantity, market_order.price())
        return order.get_status(self.__client)

    def __str__(self) -> str:
        return 'Sell strategy'


class BuyStrategy(TradeStrategy):
    def __init__(self, client: TradeClient):
        self.__client = client

    def run(self, quantity: float) -> str:
        market_order = self.__client.buy_market_order(quantity)
        order = self.__client.sell_oco_order(quantity, market_order.price())
        return order.get_status(self.__client)

    def __str__(self):
        return 'Buy strategy'
