from nodes.node import Node
from models.token import Token


class NumberNode(Node):
    def __init__(self, token: Token):
        super().__init__(token)
