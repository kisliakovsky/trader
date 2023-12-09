from _decimal import Decimal
from unittest import TestCase

from bot.trade_client import BasicTradeClient, MarketOrder, LimitMakerOrder
from client_stub import ClientStub


class TestTradeClient(TestCase):

    def setUp(self) -> None:
        self.__trade_client = BasicTradeClient(
            ClientStub(),
            Decimal(1.0005),
            Decimal(0.9995),
            Decimal(1.0005),
            Decimal(0.9995)
        )

    def test_buy_market_order(self):
        self.assertEqual(
            MarketOrder(19744496177, "FILLED", "21472.15000000"),
            self.__trade_client.buy_market_order(0.00088000)
        )

    def test_sell_market_order(self):
        self.assertEqual(
            MarketOrder(19744496177, "FILLED", "21472.15000000"),
            self.__trade_client.sell_market_order(0.00088000)
        )

    def test_sell_oco_order(self):
        self.assertEqual(
            LimitMakerOrder(19747264211),
            self.__trade_client.sell_oco_order(0.00088000, "21472.15000000")
        )

    def test_buy_oco_order(self):
        self.assertEqual(
            LimitMakerOrder(19747264211),
            self.__trade_client.buy_oco_order(0.00088000, "21472.15000000")
        )

    def test_poll_terminal_status(self):
        self.assertEqual('FILLED', self.__trade_client.poll_terminal_order_status(19747264211))
