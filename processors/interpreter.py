from models.token import *
from nodes.bin_op_node import BinOpNode
from nodes.node import Node
from nodes.number_node import NumberNode
from nodes.unary_op_node import UnaryOpNode
from values.number import Number


class Interpreter:
    def traverse(self, node: Node):
        """
        Traverse AST rooted at `node`.
        """
        # Find the appropriate method based on node type
        traverse_method_name = f"traverse_{type(node).__name__}"
        traverse_method = getattr(self, traverse_method_name, self.traverse_fallback)
        # Execute method
        return traverse_method(node)

    def traverse_NumberNode(self, node: NumberNode):
        token = node.token
        return Number(token.value, token.interval)

    def traverse_BinOpNode(self, node: BinOpNode):
        left: Number = self.traverse(node.left)
        right: Number = self.traverse(node.right)

        op_type = node.token.type
        if op_type == TOKEN_PLUS:
            result = left.add(right)
        elif op_type == TOKEN_MINUS:
            result = left.subtract(right)
        elif op_type == TOKEN_MULTIPLY:
            result = left.multiply(right)
        elif op_type == TOKEN_DIVISION:
            result = left.divide(right)
        else:
            raise Exception(f"Unknown token type '{op_type}' not handled by parser.")

        result.interval = node.interval
        return result

    def traverse_UnaryOpNode(self, node: UnaryOpNode):
        result = self.traverse(node.child)

        if node.token.type == TOKEN_MINUS:
            result = Number(0).subtract(result)

        result.interval = node.interval
        return result

    def traverse_fallback(self, node):
        raise Exception(f"No method for {type(node).__name__} defined.")
