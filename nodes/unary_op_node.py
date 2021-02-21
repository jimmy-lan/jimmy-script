from models.position import Interval
from nodes.node import Node
from models.token import Token


class UnaryOpNode(Node):
    def __init__(self, token: Token, child: Node):
        super().__init__(token)
        self.child = child
        self.interval = Interval(token.interval.start, child.interval.end, token.interval.file)

    def __repr__(self):
        return f"({self.token}, {self.child})"
