from models.position import Interval
from nodes.node import Node
from models.token import Token


class BinOpNode(Node):
    def __init__(self, token: Token, left: Node, right: Node):
        super().__init__(token)
        self.left = left
        self.right = right
        self.interval = Interval(left.interval.start, right.interval.end)

    def __repr__(self):
        return f"({self.left}, {self.token}, {self.right})"
