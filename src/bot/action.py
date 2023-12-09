import sys
import time
from abc import ABC
from logging import Logger

from counter import Counter


class Action(ABC):

    def run(self):
        pass


class LimitAction:
    def __init__(self, limit: int, action: Action):
        self.__limit = limit
        self.__action = action

    def run(self, counter: Counter):
        if counter.is_greater_or_equal(self.__limit):
            self.__action.run()

    def reset_and_run(self, counter: Counter):
        if counter.is_greater_or_equal(self.__limit):
            counter.reset()
            self.__action.run()


class LoggingAction(Action):
    def __init__(self, action: Action, logger: Logger):
        self.__action = action
        self.__logger = logger

    def run(self):
        self.__logger.debug('Running action %s', str(self.__action))
        self.__action.run()


class Sleep(Action):
    def __init__(self, duration_in_sec: int):
        self.__duration_in_sec = duration_in_sec

    def run(self):
        time.sleep(self.__duration_in_sec)

    def __str__(self):
        return f'Sleep, duration {self.__duration_in_sec} sec'


class Exit(Action):

    def run(self):
        sys.exit()

    def __str__(self):
        return 'Exit'


class NoopAction(Action):

    def run(self):
        pass

    def __str__(self):
        return 'Noop'
