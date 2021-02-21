from models.position import Interval

################################
# CONSTANTS RELATING TO TOKEN
################################
TOKEN_INT = "INT"
TOKEN_FLOAT = "FLOAT"

TOKEN_PLUS = "PLUS"
TOKEN_MINUS = "MINUS"
TOKEN_MULTIPLY = "MULTIPLY"
TOKEN_DIVISION = "DIVISION"
TOKEN_POWER = "POWER"

TOKEN_LBRACKET = "LBRACKET"
TOKEN_RBRACKET = "RBRACKET"

TOKEN_IDENTIFIER = "IDENTIFIER"
TOKEN_KEYWORD = "KEYWORD"
TOKEN_ASSIGNMENT = "ASSIGNMENT"

TOKEN_EOF = "EOF"

TOKEN_MAP = {
    "+": TOKEN_PLUS,
    "-": TOKEN_MINUS,
    "*": TOKEN_MULTIPLY,
    "/": TOKEN_DIVISION,
    "^": TOKEN_POWER,
    "(": TOKEN_LBRACKET,
    ")": TOKEN_RBRACKET,
}

NUMBER_TOKENS = (TOKEN_INT, TOKEN_FLOAT)
TERM_TOKENS = (TOKEN_PLUS, TOKEN_MINUS)
EXPR_TOKENS = (TOKEN_MULTIPLY, TOKEN_DIVISION)

ASSIGNMENT_OP = ["=", "<-", "be"]
KEYWORDS = [
    "let"
]


################################
# TOKEN REPRESENTATION
################################

class Token:
    # Type of token.
    type: str
    # Value of token
    value: any
    # The interval in a file containing this token
    interval: Interval

    @staticmethod
    def map_char_to_type(char: str):
        return TOKEN_MAP[char]

    @staticmethod
    def is_op_char(char: str):
        return char in TOKEN_MAP

    def __init__(self, t_type: str, value: any = None, interval: Interval = None) -> None:
        self.type = t_type
        self.value = value
        self.interval = interval

    def __repr__(self) -> str:
        return f"{self.type}: {self.value}" if self.value else f"{self.type}"

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value
