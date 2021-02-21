from models.token import *
from nodes.bin_op_node import BinOpNode
from nodes.node import Node
from nodes.number_node import NumberNode
from nodes.unary_op_node import UnaryOpNode
from processors.promises import InterpreterPromise
from values.number import Number


class Interpreter:
    def traverse(self, node: Node) -> InterpreterPromise:
        """
        Traverse AST rooted at `node`.
        """
        # Find the appropriate method based on node type
        traverse_method_name = f"traverse_{type(node).__name__}"
        traverse_method = getattr(self, traverse_method_name, self.traverse_fallback)
        # Execute method
        return traverse_method(node)

    def traverse_NumberNode(self, node: NumberNode) -> InterpreterPromise:
        token = node.token
        return InterpreterPromise().resolve(Number(token.value, token.interval))

    def traverse_BinOpNode(self, node: BinOpNode) -> InterpreterPromise:
        promise = InterpreterPromise()
        left: Number = promise.register(self.traverse(node.left))
        if promise.error:
            return promise
        right: Number = promise.register(self.traverse(node.right))
        if promise.error:
            return promise

        op_type = node.token.type
        if op_type == TOKEN_PLUS:
            result, error = left.add(right)
        elif op_type == TOKEN_MINUS:
            result, error = left.subtract(right)
        elif op_type == TOKEN_MULTIPLY:
            result, error = left.multiply(right)
        elif op_type == TOKEN_DIVISION:
            result, error = left.divide(right)
        else:
            raise Exception(f"Unknown token type '{op_type}' not handled by parser.")

        if error is not None:
            return promise.reject(error)

        result.interval = node.interval
        return promise.resolve(result)

    def traverse_UnaryOpNode(self, node: UnaryOpNode) -> InterpreterPromise:
        promise = InterpreterPromise()
        result = promise.register(self.traverse(node.child))
        if promise.error:
            return promise

        if node.token.type == TOKEN_MINUS:
            result, error = Number(0).subtract(result)
            if error is not None:
                return promise.reject(error)

        result.interval = node.interval
        return promise.resolve(result)

    def traverse_fallback(self, node) -> None:
        raise Exception(f"No method for {type(node).__name__} defined.")
