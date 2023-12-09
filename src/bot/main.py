"""This script runs the application"""
from logging import DEBUG
from _decimal import Decimal

from binance.client import Client as BinanceClient

from binance_client import LoggingBinanceClient, MarginClient, SpotClient, RetryClient
from action import Sleep, NoopAction, LoggingAction, LimitAction, Exit
from logger_factory import LoggerFactory
from trade_bot import TradeBot
from trade_client import BasicTradeClient, LoggingTradeClient, RecoveringTradeClient
from trade_strategy import CycleTradeStrategySupplier, BuyStrategy, SellStrategy, LoggingTradeStrategySupplier

logger_factory = LoggerFactory('%(asctime)s %(name)s: %(message)s', DEBUG)
red_logger_factory = LoggerFactory("\x1b[31;20m%(asctime)s %(name)s: %(message)s\x1b[0m", DEBUG)
trade_client = LoggingTradeClient(
    RecoveringTradeClient(
        BasicTradeClient(
            client=LoggingBinanceClient(
                RetryClient(
                    SpotClient(
                        BinanceClient(
                            'api-key',
                            'api-secret'
                        )
                    )
                ),
                logger_factory.logger('Binance client        ')
            ),
            sell_raise_coefficient=Decimal(1.0005),
            sell_decrease_coefficient=Decimal(0.9995),
            buy_raise_coefficient=Decimal(1.0005),
            buy_decrease_coefficient=Decimal(0.9995)
        )
    ),
    logger_factory.logger('Trade client          ')
)
TradeBot(
    strategy_supplier=LoggingTradeStrategySupplier(
        CycleTradeStrategySupplier(
            [
                BuyStrategy(trade_client),
                SellStrategy(trade_client)
            ]
        ),
        logger_factory.logger('Strategy supplier     ')
    ),
    strategy_changes_limit=LimitAction(5, LoggingAction(Sleep(600), logger_factory.logger('Strategy change action'))),
    expiration_limit=LimitAction(1, LoggingAction(Exit(), logger_factory.logger('Expiration action     '))),
    logger=red_logger_factory.logger('Bot                   ')
).start(0.00088000)
