from models.token import Token
from nodes.node import Node


class VarAssignNode(Node):
    def __init__(self, token: Token):
        super(VarAssignNode, self).__init__(token)
