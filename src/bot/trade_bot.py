"""This module contains a bot that can trade with a special client following special strategies"""
from logging import Logger

from action import LimitAction
from quantity import Quantity
from counter import Counter
from trade_strategy import TradeStrategySupplier


class TradeBot:
    def __init__(
            self,
            strategy_supplier: TradeStrategySupplier,
            strategy_changes_limit: LimitAction,
            expiration_limit: LimitAction,
            logger: Logger
    ):
        self.__strategy_changes_in_a_row_counter = Counter(0)
        self.__strategy_supplier = strategy_supplier
        self.__strategy_changes_limit = strategy_changes_limit
        self.__expiration_limit = expiration_limit
        self.__logger = logger
        self.__run_counter = Counter(1)
        self.__filled_counter = Counter(0)
        self.__expired_counter = Counter(0)

    def start(self, quantity: Quantity):
        strategy = self.__strategy_supplier.next_strategy()
        while True:
            self.__logger.debug("Run %s, strategy %s", str(self.__run_counter), str(strategy))
            self.__logger.debug(
                "Orders filled %s, expired %s",
                str(self.__filled_counter),
                str(self.__expired_counter)
            )
            status = strategy.run(quantity)
            self.__run_counter.inc()
            if status == 'FILLED':
                self.__filled_counter.inc()
                self.__strategy_changes_in_a_row_counter.reset()
                quantity.reset()
            elif status == 'EXPIRED':
                self.__expired_counter.inc()
                self.__expiration_limit.run(self.__expired_counter)
                next_strategy = self.__strategy_supplier.next_strategy()
                if strategy != next_strategy:
                    self.__strategy_changes_in_a_row_counter.inc()
                    self.__strategy_changes_limit.reset_and_run(self.__strategy_changes_in_a_row_counter)
                strategy = next_strategy
                quantity.double()
            else:
                raise ValueError(f"Unknown order status: {status}. I'm stopping.")
