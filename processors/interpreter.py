from nodes.bin_op_node import BinOpNode
from nodes.node import Node
from nodes.number_node import NumberNode
from nodes.unary_op_node import UnaryOpNode


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
        print("number node")

    def traverse_BinOpNode(self, node: BinOpNode):
        print("bin op node")
        self.traverse(node.left)
        self.traverse(node.right)

    def traverse_UnaryOpNode(self, node: UnaryOpNode):
        print("unary op node")
        self.traverse(node.child)

    def traverse_fallback(self, node):
        raise Exception(f"No method for {type(node).__name__} defined.")
