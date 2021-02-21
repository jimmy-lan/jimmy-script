from errors.interpret_error import InterpretError
from models.context import ExecutionContext
from models.token import *
from nodes.bin_op_node import BinOpNode
from nodes.node import Node
from nodes.number_node import NumberNode
from nodes.unary_op_node import UnaryOpNode
from nodes.var_access_node import VarAccessNode
from nodes.var_assign_node import VarAssignNode
from processors.promises import InterpreterPromise
from values.number import Number


class Interpreter:
    def traverse(self, node: Node, context: ExecutionContext) -> InterpreterPromise:
        """
        Traverse AST rooted at `node`.
        """
        # Find the appropriate method based on node type
        traverse_method_name = f"traverse_{type(node).__name__}"
        traverse_method = getattr(self, traverse_method_name, self.traverse_fallback)
        # Execute method
        return traverse_method(node, context)

    def traverse_NumberNode(self, node: NumberNode, context: ExecutionContext) -> InterpreterPromise:
        token = node.token
        return InterpreterPromise().resolve(Number(token.value, token.interval, context))

    def traverse_BinOpNode(self, node: BinOpNode, context: ExecutionContext) -> InterpreterPromise:
        promise = InterpreterPromise()
        left: Number = promise.register(self.traverse(node.left, context))
        if promise.error:
            return promise
        right: Number = promise.register(self.traverse(node.right, context))
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
        elif op_type == TOKEN_POWER:
            result, error = left.power(right)
        else:
            raise Exception(f"Unknown token type '{op_type}' not handled by parser.")

        if error is not None:
            return promise.reject(error)

        result.interval = node.interval
        return promise.resolve(result)

    def traverse_UnaryOpNode(self, node: UnaryOpNode, context: ExecutionContext) -> InterpreterPromise:
        promise = InterpreterPromise()
        result = promise.register(self.traverse(node.child, context))
        if promise.error:
            return promise

        if node.token.type == TOKEN_MINUS:
            result, error = Number(0).subtract(result)
            if error is not None:
                return promise.reject(error)

        result.interval = node.interval
        return promise.resolve(result)

    def traverse_VarAccessNode(self, node: VarAccessNode, context: ExecutionContext):
        promise = InterpreterPromise()
        identifier = node.token.value
        var_value = context.variable_register.get(identifier)
        if var_value is None:
            return promise.reject(InterpretError(f"Unknown identifier '{identifier}'.", node.interval, context))

        var_value: Number = var_value.copy()
        var_value.interval = node.interval
        return promise.resolve(var_value)

    def traverse_VarAssignNode(self, node: VarAssignNode, context: ExecutionContext):
        promise = InterpreterPromise()
        identifier = node.token.value
        var_value = promise.register(self.traverse(node.value_node, context))
        if promise.error:
            return promise

        context.variable_register.set(identifier, var_value)
        return promise.resolve(None)

    def traverse_fallback(self, node) -> None:
        raise Exception(f"No method for {type(node).__name__} defined.")
