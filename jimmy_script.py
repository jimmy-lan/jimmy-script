# Token Types
from typing import Tuple, List, Iterable

TOKEN_INT = "INT"
TOKEN_FLOAT = "FLOAT"
TOKEN_PLUS = "PLUS"
TOKEN_MINUS = "MINUS"
TOKEN_MULTIPLY = "MULTIPLY"
TOKEN_DIVISION = "DIVISION"
TOKEN_LBRACKET = "LBRACKET"
TOKEN_RBRACKET = "RBRACKET"
TOKEN_EOF = "EOF"

SPACES = " \t"
NEW_LINE = "\n"
DIGITS = "0123456789"
CHAR_TO_TOKEN = {
    "+": TOKEN_PLUS,
    "-": TOKEN_MINUS,
    "*": TOKEN_MULTIPLY,
    "/": TOKEN_DIVISION,
    "(": TOKEN_LBRACKET,
    ")": TOKEN_RBRACKET
}

NUMBER_TOKENS = (TOKEN_INT, TOKEN_FLOAT)


class Position:
    def __init__(self, idx: int, row: int, col: int, fn: str) -> None:
        self.idx = idx
        self.row = row
        self.col = col
        self.fn = fn

    def next(self, curr: str = None):
        self.idx += 1

        if curr == NEW_LINE:
            self.row += 1
            self.col = 0
        else:
            self.col += 1

        return self

    def copy(self):
        return Position(self.idx, self.row, self.col, self.fn)


class Token:
    def __init__(self, t_type: str, value: any = None, pos: Position = None,) -> None:
        self.type = t_type
        self.value = value
        self.pos = pos

    def __repr__(self) -> str:
        return f"{self.type}: {self.value}" if self.value else f"{self.type}"


class Error:
    def __init__(self, name: str, msg: str, pos: Position) -> None:
        self.name = name
        self.msg = msg
        self.pos = pos

    def __str__(self) -> str:
        return f"{self.name}: \n\t{self.msg}\nAt Line {self.pos.row + 1} in File {self.pos.fn}."


class UnexpectedTokenError(Error):
    def __init__(self, msg: str, pos: Position) -> None:
        super().__init__("Unexpected Token", msg, pos)


class BadSyntaxError(Error):
    def __init__(self, msg: str, pos: Position) -> None:
        super().__init__("Bad Syntax", msg, pos)


class Lexer:
    def __init__(self, raw: str, fn: str) -> None:
        self.raw = raw
        self.pos = Position(0, 0, 0, fn)
        self.curr = raw[0] if len(raw) > 0 else None

    def next(self) -> None:
        self.pos.next(self.curr)
        idx = self.pos.idx
        if idx < len(self.raw):
            self.curr = self.raw[idx]
        else:
            self.curr = None

    def get_tokens(self) -> Tuple[List[Token], Error or None]:
        tokens = []

        while self.curr is not None:
            if self.curr in SPACES:
                # Ignore, go to the next token
                self.next()
            elif self.curr in DIGITS:
                tokens.append(self.get_number())
            elif self.curr in CHAR_TO_TOKEN:
                tokens.append(Token(CHAR_TO_TOKEN[self.curr], pos=self.pos))
                self.next()
            else:
                token = self.curr
                pos = self.pos.col
                self.next()
                return [], UnexpectedTokenError(
                    f"Unexpected token '{token}' at position {pos}.",
                    self.pos
                )

        tokens.append(Token(TOKEN_EOF, pos=self.pos))
        return tokens, None

    def get_number(self) -> Token:
        parsed_str = ""
        num_dots = 0
        pos = self.pos.copy()

        while self.curr is not None and self.curr in DIGITS + ".":
            if self.curr == ".":
                if num_dots > 0:
                    break
                num_dots += 1
            parsed_str += self.curr
            self.next()

        if num_dots == 0:
            return Token(TOKEN_INT, int(parsed_str), pos)
        else:
            return Token(TOKEN_FLOAT, float(parsed_str), pos)


class Node:
    def __init__(self, token: Token):
        self.token = token

    def __repr__(self):
        return str(self.token)


class NumberNode(Node):
    def __init__(self, token: Token):
        super().__init__(token)


class BinOpNode(Node):
    def __init__(self, token: Token, left: Node, right: Node):
        super().__init__(token)
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.left}, {self.token}, {self.right})"


class UnaryOpNode(Node):
    def __init__(self, token: Token, child: Node):
        super().__init__(token)
        self.child = child

    def __repr__(self):
        return f"({self.token}, {self.child})"


class ParserPromise:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, p):
        if isinstance(p, ParserPromise):
            if p.error is not None:
                self.error = p.error
            return p.node
        return p

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
            return promise.reject(BadSyntaxError("Invalid expression. Expecting at least one operator.", self.curr.pos))
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
                return promise.reject(BadSyntaxError("Missing ')'.", self.curr.pos))
        return promise.reject(BadSyntaxError(f"Expecting a number, got '{token}'.", token.pos))

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

    def bin_op(self, func, operations: Iterable[str]) -> ParserPromise:
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


def execute(raw: str, fn: str):
    # Get tokens from laxer
    lexer = Lexer(raw, fn)
    tokens, error = lexer.get_tokens()
    if error:
        return None, error

    # Get abstract syntax tree
    parser = Parser(tokens)
    ast = parser.parse()

    return ast.node, ast.error
