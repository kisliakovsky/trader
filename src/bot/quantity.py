"""This module contains a quantity implementation"""


class Quantity:
    def __init__(self, init_value: float):
        self.__init_value = init_value
        self.__quantity = init_value

    def double(self):
        self.__quantity = self.__quantity * 2

    def multiply(self, multiplier: float):
        self.__quantity = self.__quantity * multiplier

    def reset(self):
        self.__quantity = self.__init_value

    def float_value(self) -> float:
        return self.__quantity

    def __str__(self) -> str:
        return str(self.__quantity)
