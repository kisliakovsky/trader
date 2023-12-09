from _decimal import Decimal
from unittest import TestCase

from bot.trade_client import BasicTradeClient
from bot.trade_strategy import CycleTradeStrategySupplier, BuyStrategy, SellStrategy
from client_stub import ClientStub


class TestCycleTradeStrategySupplier(TestCase):

    def setUp(self) -> None:
        trade_client = BasicTradeClient(
            ClientStub(),
            Decimal(1.0005),
            Decimal(0.9995),
            Decimal(1.0005),
            Decimal(0.9995)
        )
        self.__supplier = CycleTradeStrategySupplier(
            [
                BuyStrategy(trade_client),
                SellStrategy(trade_client)
            ]
        )

    def test_next_strategy(self):
        self.assertIsInstance(
            self.__supplier.next_strategy(),
            BuyStrategy
        )
        self.assertIsInstance(
            self.__supplier.next_strategy(),
            SellStrategy
        )
        self.assertIsInstance(
            self.__supplier.next_strategy(),
            BuyStrategy
        )
        self.assertIsInstance(
            self.__supplier.next_strategy(),
            SellStrategy
        )
