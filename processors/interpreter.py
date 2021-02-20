from nodes.bin_op_node import BinOpNode
from nodes.node import Node
from nodes.number_node import NumberNode
from nodes.unary_op_node import UnaryOpNode


class Interpreter:
    def traverse(self, node: Node):
        method_name = f"traverse_{type(node).__name__}"
        method = getattr(self, method_name, self.traverse_fallback)
        return method(node)

    def traverse_NumberNode(self, node: NumberNode):
        print("number node")

    def traverse_BinOpNode(self, node: BinOpNode):
        print("bin op node")

    def traverse_UnaryOpNode(self, node: UnaryOpNode):
        print("unary op node")

    def traverse_fallback(self, node):
        raise Exception(f"No method for {type(node).__name__} defined.")
