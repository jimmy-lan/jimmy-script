from models.position import Interval
from models.variable_register import VariableRegister


class ExecutionContext:
    """
    An execution context represents where a piece of code is
    executed. By keeping track of execution context, we can
    display more meaningful error messages to users.
    """
    # Name of context
    name: str
    # Parent context
    parent: any
    # Parent code position
    parent_interval: Interval
    # Variable table
    variable_register: VariableRegister or None

    def __init__(self, name: str, parent: any = None, parent_interval: Interval = None):
        self.name = name
        self.parent_interval = parent_interval
        self.parent = parent
        self.variable_register = None
