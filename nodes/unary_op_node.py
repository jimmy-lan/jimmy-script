from nodes.node import Node
from token import Token


class UnaryOpNode(Node):
    def __init__(self, token: Token, child: Node):
        super().__init__(token)
        self.child = child

    def __repr__(self):
        return f"({self.token}, {self.child})"
