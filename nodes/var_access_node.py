from models.token import Token
from nodes.node import Node


class VarAccessNode(Node):
    def __init__(self, token: Token):
        super(VarAccessNode, self).__init__(token)
