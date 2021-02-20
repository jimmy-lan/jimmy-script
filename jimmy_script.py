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


class Token:
    def __init__(self, t_type: str, value: any = None) -> None:
        self.type = t_type
        self.value = value

    def __repr__(self) -> str:
        return f"{self.type}: {self.value}" if self.value else f"{self.type}"


class Position:
    def __init__(self, idx: int, row: int, col: int, fn: str) -> None:
        self.idx = idx
        self.row = row
        self.col = col
        self.fn = fn

    def next(self, curr: str):
        self.idx += 1

        if curr == NEW_LINE:
            self.row += 1
            self.col = 0
        else:
            self.col += 1

        return self

    def copy(self):
        return Position(self.idx, self.row, self.col, self.fn)


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
                tokens.append(Token(CHAR_TO_TOKEN[self.curr]))
                self.next()
            else:
                token = self.curr
                pos = self.pos.col
                self.next()
                return [], UnexpectedTokenError(
                    f"Unexpected token '{token}' at position {pos}.",
                    self.pos
                )

        return tokens, None

    def get_number(self) -> Token:
        parsed_str = ""
        num_dots = 0

        while self.curr is not None and self.curr in DIGITS + ".":
            if self.curr == ".":
                if num_dots > 0:
                    break
                num_dots += 1
            parsed_str += self.curr
            self.next()

        if num_dots == 0:
            return Token(TOKEN_INT, int(parsed_str))
        else:
            return Token(TOKEN_FLOAT, float(parsed_str))


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


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.curr = tokens[0] if len(tokens) > 0 else None

    def next(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.curr = self.tokens[self.pos]

    def parse(self):
        return self.expr()

    def factor(self):
        """
        Return a node representation of a factor.
        A factor is a single point of data.
        For example, "5" by itself is a factor in a expression.
        """
        token = self.curr
        if token.type in NUMBER_TOKENS:
            self.next()
            return NumberNode(token)

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

    def bin_op(self, func, operations: Iterable[str]) -> BinOpNode:
        left = func()
        while self.curr.type in operations:
            token = self.curr
            self.next()
            right = func()
            # Merge to binary operation tree
            left = BinOpNode(token, left, right)

        return left


def execute(raw: str, fn: str):
    # Get tokens from laxer
    lexer = Lexer(raw, fn)
    tokens, error = lexer.get_tokens()
    if error:
        return None, error

    # Get abstract syntax tree
    parser = Parser(tokens)
    ast = parser.parse()

    return ast, None
