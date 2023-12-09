"""This module contains a plain counter implementation"""


class Counter:
    def __init__(self, init_value: int):
        self.__counter = init_value

    def inc(self):
        self.__counter = self.__counter + 1

    def reset(self):
        self.__counter = 0

    def is_greater_or_equal(self, value: int) -> bool:
        return self.__counter >= value

    def is_less_or_equal(self, value: int) -> bool:
        return self.__counter <= value

    def __str__(self) -> str:
        return str(self.__counter)
