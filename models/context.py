from models.position import Position


class ExecutionContext:
    """
    An execution context represents where a piece of code is
    executed. By keeping track of execution context, we can
    display more meaningful error messages to users.
    """
    # Name of context
    name: str
    # Parent of context
    parent: any
    # Parent code position
    parent_pos: Position

    def __init__(self, name: str, parent: any = None, parent_pos: Position = None):
        self.name = name
        self.parent_pos = parent_pos
        self.parent = parent
