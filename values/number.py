from typing import Optional

from errors.interpret_error import InterpretError
from models.context import ExecutionContext
from models.position import Interval


class Number:
    """
    A class to hold a numeric value.
    """
    # Value to hold
    value: int or float
    # Interval where this number occupies in Jimmy Script code file
    interval: Optional[Interval]
    # Execution context
    context: ExecutionContext

    def __init__(self, value: int or float, interval: Interval = None, context: ExecutionContext = None):
        self.value = value
        self.interval = interval
        self.context = context

    def add(self, other):
        if not isinstance(other, Number):
            return
        return Number(self.value + other.value, context=self.context), None

    def subtract(self, other):
        if not isinstance(other, Number):
            return
        return Number(self.value - other.value, context=self.context), None

    def multiply(self, other):
        if not isinstance(other, Number):
            return
        return Number(self.value * other.value, context=self.context), None

    def divide(self, other):
        if not isinstance(other, Number):
            return
        if other.value == 0:
            return None, InterpretError("Cannot divide by 0.", other.interval, self.context)
        return Number(self.value / other.value, context=self.context), None

    def power(self, other):
        if not isinstance(other, Number):
            return
        return Number(self.value ** other.value, context=self.context), None

    def __repr__(self):
        return str(self.value)
