from typing import Optional

from models.position import Interval


class Number:
    """
    A class to hold a numeric value.
    """
    # Value to hold
    value: int or float
    # Interval where this number occupies in Jimmy Script code file
    interval: Optional[Interval]

    def __init__(self, value: int or float, interval: Interval = None):
        self.value = value
        self.interval = interval

    def add(self, other):
        if not isinstance(other, Number):
            return
        return Number(self.value + other.value)

    def subtract(self, other):
        if not isinstance(other, Number):
            return
        return Number(self.value - other.value)

    def multiply(self, other):
        if not isinstance(other, Number):
            return
        return Number(self.value * other.value)

    def divide(self, other):
        if not isinstance(other, Number):
            return
        return Number(self.value / other.value)

    def __repr__(self):
        return str(self.value)
