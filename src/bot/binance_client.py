"""This module contains a wrapper with logging and exception handling over basic Binance client"""

from logging import Logger

from binance.exceptions import BinanceAPIException
from urllib3.exceptions import ReadTimeoutError

from counter import Counter


class LoggingBinanceClient:
    def __init__(self, binance_client, logger: Logger):
        self.__binance_client = binance_client
        self.__logger = logger

    def create_order(self, **params) -> str:
        self.__logger.debug('Making the order %s', params)
        try:
            response = self.__binance_client.create_order(**params)
        except Exception as exception:
            raise OrderException('Failed to make the order') from exception
        return response

    def create_oco_order(self, **params) -> str:
        self.__logger.debug('Making the OCO order %s', params)
        try:
            response = self.__binance_client.create_oco_order(**params)
        except BinanceAPIException as binance_exception:
            code = binance_exception.code
            message = binance_exception.message
            if code == -2010 and 'The relationship of the prices for the orders is not correct' in message:
                raise PriceOcoOrderException(
                    'The relationship of the prices for the orders is not correct'
                ) from binance_exception
            raise OcoOrderException('Failed to make the OCO order') from binance_exception
        except Exception as exception:
            raise OcoOrderException('Failed to make the OCO order') from exception
        return response

    def get_order(self, **params) -> str:
        self.__logger.debug('Getting the order %s', params)
        try:
            response = self.__binance_client.get_order(**params)
        except Exception as exception:
            raise GetOrderException('Failed to get the order') from exception
        return response


class RetryClient:
    def __init__(self, binance_client):
        self.__binance_client = binance_client
        self.__retry_limit = 3

    def create_order(self, **params) -> str:
        return self.__binance_client.create_order(**params)

    def create_oco_order(self, **params) -> str:
        return self.__binance_client.create_oco_order(**params)

    def get_order(self, **params) -> str:
        retry_attempt = Counter(1)
        while retry_attempt.is_less_or_equal(self.__retry_limit):
            try:
                return self.__binance_client.get_order(**params)
            except ReadTimeoutError:
                retry_attempt.inc()
        raise GetOrderException("Retry limit exceeded")


class SpotClient:
    def __init__(self, binance_client):
        self.__binance_client = binance_client

    def create_order(self, **params) -> str:
        return self.__binance_client.create_order(**params)

    def create_oco_order(self, **params) -> str:
        return self.__binance_client.create_oco_order(**params)

    def get_order(self, **params) -> str:
        return self.__binance_client.get_order(**params)


class MarginClient:
    def __init__(self, binance_client):
        self.__binance_client = binance_client

    def create_order(self, **params) -> str:
        return self.__binance_client.create_margin_order(**params)

    def create_oco_order(self, **params) -> str:
        return self.__binance_client.create_margin_oco_order(**params)

    def get_order(self, **params) -> str:
        return self.__binance_client.get_margin_order(**params)


class BinanceClientException(Exception):
    def __init__(self, message: str):
        self.__message = message
        super().__init__(self.__message)


class OrderException(BinanceClientException):
    def __init__(self, message: str):
        self.__message = message
        super().__init__(self.__message)


class OcoOrderException(BinanceClientException):
    def __init__(self, message: str):
        self.__message = message
        super().__init__(self.__message)


class PriceOcoOrderException(OcoOrderException):
    def __init__(self, message: str):
        self.__message = message
        super().__init__(self.__message)


class GetOrderException(BinanceClientException):
    def __init__(self, message: str):
        self.__message = message
        super().__init__(self.__message)
