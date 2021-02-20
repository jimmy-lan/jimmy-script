from nodes.node import Node
from token import Token


class BinOpNode(Node):
    def __init__(self, token: Token, left: Node, right: Node):
        super().__init__(token)
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.left}, {self.token}, {self.right})"
