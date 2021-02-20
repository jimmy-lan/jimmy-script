# Token Types
TOKEN_INT = "INT"
TOKEN_FLOAT = "FLOAT"
TOKEN_PLUS = "PLUS"
TOKEN_MINUS = "MINUS"
TOKEN_MULTIPLY = "MULTIPLY"
TOKEN_DIVISION = "DIVISION"
TOKEN_LBRACKET = "LBRACKET"
TOKEN_RBRACKET = "RBRACKET"

SPACES = " \t"
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
    def __init__(self, t_type: str, value: any) -> None:
        self.type = t_type
        self.value = value

    def __repr__(self) -> str:
        return f"{self.type}: {self.value}" if self.value else f"{self.type}"


class Lexer:
    def __init__(self, expr: str) -> None:
        self.expr = expr
        self.pos = -1
        self.curr = None

    def next(self) -> None:
        self.pos += 1
        if self.pos < len(self.expr):
            self.curr = self.expr[self.pos]
        else:
            self.curr = None

    def get_tokens(self):
        tokens = []

        while self.curr is not None:
            if self.curr in SPACES:
                self.next()
            elif self.curr in DIGITS:
                self.get_number()
            elif self.curr in CHAR_TO_TOKEN:
                tokens.append(CHAR_TO_TOKEN[self.curr])
                self.next()

    def get_number(self):
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
