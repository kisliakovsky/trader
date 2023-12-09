"""This module contains a default logger factory"""

import logging
import sys
from logging import Logger, StreamHandler, Formatter


class LoggerFactory:
    def __init__(self, format: str, level: int):
        self.__format = format
        self.__level = level

    def logger(self, name: str) -> Logger:
        stream_handler = StreamHandler(stream=sys.stdout)
        stream_handler.setFormatter(Formatter(self.__format))
        logger = logging.getLogger(name)
        logger.setLevel(self.__level)
        logger.addHandler(stream_handler)
        return logger
