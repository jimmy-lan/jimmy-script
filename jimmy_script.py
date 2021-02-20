# Token Types
from typing import Tuple, List

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
    def __init__(self, expr: str, fn: str) -> None:
        self.expr = expr
        self.pos = Position(0, 0, 0, fn)
        self.curr = expr[0] if len(expr) > 0 else None

    def next(self) -> None:
        self.pos.next(self.curr)
        idx = self.pos.idx
        if idx < len(self.expr):
            self.curr = self.expr[idx]
        else:
            self.curr = None

    def get_tokens(self) -> Tuple[List[str], Error or None]:
        tokens = []

        while self.curr is not None:
            if self.curr in SPACES:
                self.next()
            elif self.curr in DIGITS:
                tokens.append(self.get_number())
            elif self.curr in CHAR_TO_TOKEN:
                tokens.append(CHAR_TO_TOKEN[self.curr])
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
    def __init__(self, token: any):
        self.token = token

    def __repr__(self):
        return str(self.token)


class NumberNode(Node):
    def __init__(self, token: int or float):
        super().__init__(token)


class BinOpNode(Node):
    def __init__(self, token: str, left: Node, right: Node):
        super().__init__(token)
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.left}, {self.token}, {self.right})"


def evaluate(expr: str, fn: str) -> Tuple[List[str], Error or None]:
    lexer = Lexer(expr, fn)
    return lexer.get_tokens()
