from models.token import Token
from nodes.node import Node


class VarAssignNode(Node):
    def __init__(self, token: Token, value_node: Node):
        """
        :param value_node: The node corresponding to the part of expression
            on the right side of the assignment operator.
        """
        super(VarAssignNode, self).__init__(token)
        self.value_node = value_node
