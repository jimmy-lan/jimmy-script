from typing import List

from errors.bad_syntax_error import BadSyntaxError
from nodes.bin_op_node import BinOpNode
from nodes.number_node import NumberNode
from nodes.unary_op_node import UnaryOpNode
from models.token import *
from processors.promises import ParserPromise


class Parser:
    """
    A parser takes in a list of tokens and parse the tokens
    into a abstract syntax tree.
    """
    # Tokens to process
    tokens: List[Token]
    # Current index in the tokens array
    curr_idx: int
    # Current token being processed
    curr: Token or None

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

    def atom(self):
        """
        An "atom" is a number by itself or an open bracket followed by some expression then
        followed by a closing bracket.
        """
        promise = ParserPromise()
        token = self.curr

        # A bracket with some expressions in it is also considered to be
        # an "atom" node.
        if token.type == TOKEN_LBRACKET:
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

        # A number token by itself is an "atom" node
        elif token.type in NUMBER_TOKENS:
            promise.register(self.next())
            return promise.resolve(NumberNode(token))

        # A variable is considered to be an "atom" node.
        elif token.type == TOKEN_IDENTIFIER:
            promise.register(self.next())
            return promise.resolve(VarAccessNode(token))

        return promise.reject(BadSyntaxError(f"Expecting a number, sign, or bracket.", token.interval))

    def power(self):
        return self.bin_op(self.atom, [TOKEN_POWER], self.factor)

    def factor(self):
        """
        Return a node representation of a factor.
        A factor is a number with plus or minus sign.
        """
        promise = ParserPromise()
        token = self.curr

        # Additional (plus/minus) in front of a factor is
        # also considered to be a part of the factor.
        if token.type in [TOKEN_PLUS, TOKEN_MINUS]:
            promise.register(self.next())
            factor = promise.register(self.factor())
            if promise.error:
                return promise
            return promise.resolve(UnaryOpNode(token, factor))

        return self.power()

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
        promise = ParserPromise()

        # Evaluate variable assignment grammar:
        # let `identifier` = `expr`, OR,
        # let `identifier` be `expr`.
        if self.curr == Token(TOKEN_KEYWORD, "let"):
            promise.register(self.next())

            if self.curr.type != TOKEN_IDENTIFIER:
                return promise.reject(
                    BadSyntaxError("Identifier expected after let keyword.", self.curr.interval))

            identifier = self.curr
            promise.register(self.next())

            if self.curr.type != TOKEN_ASSIGNMENT or \
                    self.curr.type != TOKEN_KEYWORD:
                return promise.reject(BadSyntaxError(f"Invalid assignment operator {self.curr}.", self.curr.interval))

            promise.register(self.next())
            expr = promise.register(self.expr())
            if promise.error:
                return promise
            return promise.resolve(VarAssignNode(identifier, expr))

        return self.bin_op(self.term, [TOKEN_PLUS, TOKEN_MINUS])

    def bin_op(self, left_func, operations, right_func=None) -> ParserPromise:
        if right_func is None:
            right_func = left_func

        promise = ParserPromise()
        left = promise.register(left_func())
        if promise.error:
            return promise

        while self.curr.type in operations:
            token = self.curr
            promise.register(self.next())
            right = promise.register(right_func())
            if promise.error:
                return promise
            # Merge to binary operation tree
            left = BinOpNode(token, left, right)

        return promise.resolve(left)
