from collections import Iterable
from typing import List

from errors.bad_syntax_error import BadSyntaxError
from errors.error import Error
from nodes.bin_op_node import BinOpNode
from nodes.node import Node
from nodes.number_node import NumberNode
from nodes.unary_op_node import UnaryOpNode
from token import *


class ParserPromise:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, promise):
        if isinstance(promise, ParserPromise):
            if promise.error is not None:
                self.error = promise.error
            return promise.node
        return promise

    def resolve(self, node: Node):
        self.node = node
        return self

    def reject(self, error: Error):
        self.error = error
        return self


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.curr_idx = 0
        self.curr = tokens[0] if len(tokens) > 0 else None

    def next(self):
        self.curr_idx += 1
        if self.curr_idx < len(self.tokens):
            self.curr = self.tokens[self.curr_idx]

    def parse(self):
        promise = self.expr()
        if not promise.error and self.curr.type != TOKEN_EOF:
            error = BadSyntaxError("Invalid expression. Expecting at least one operator.", self.curr.interval)
            return promise.reject(error)
        return promise

    def factor(self):
        """
        Return a node representation of a factor.
        A factor is a single point of data.
        For example, "5" by itself is a factor in a expression.
        """
        promise = ParserPromise()
        token = self.curr
        if token.type in [TOKEN_PLUS, TOKEN_MINUS]:
            promise.register(self.next())
            factor = promise.register(self.factor())
            if promise.error:
                return promise
            return promise.resolve(UnaryOpNode(token, factor))
        elif token.type in NUMBER_TOKENS:
            promise.register(self.next())
            return promise.resolve(NumberNode(token))
        elif token.type == TOKEN_LBRACKET:
            promise.register(self.next())
            expr = promise.register(self.expr())
            if promise.error:
                return promise
            if self.curr.type == TOKEN_RBRACKET:
                promise.register(self.next())
                return promise.resolve(expr)
            else:
                error = BadSyntaxError("Missing ')'.", self.curr.interval)
                return promise.reject(error)
        return promise.reject(BadSyntaxError(f"Expecting a number, got '{token}'.", token.interval))

    def term(self):
        """
        Return a node representation of a term.
        A term is defined to be a factor multiply or divide by another
        factor.
        """
        return self.bin_op(self.factor, [TOKEN_MULTIPLY, TOKEN_DIVISION])

    def expr(self):
        """
        Return a node representation of an expression.
        A term is defined to be a factor plus or minus by another
        factor.
        """
        return self.bin_op(self.term, [TOKEN_PLUS, TOKEN_MINUS])

    def bin_op(self, func, operations) -> ParserPromise:
        promise = ParserPromise()
        left = promise.register(func())
        if promise.error:
            return promise

        while self.curr.type in operations:
            token = self.curr
            promise.register(self.next())
            right = promise.register(func())
            # Merge to binary operation tree
            left = BinOpNode(token, left, right)

        return promise.resolve(left)
