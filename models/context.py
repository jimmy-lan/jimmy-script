from models.position import Interval


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

    def __init__(self, name: str, parent: any = None, parent_interval: Interval = None):
        self.name = name
        self.parent_interval = parent_interval
        self.parent = parent
