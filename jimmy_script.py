# Token Types
TOKEN_INT = "INT"
TOKEN_FLOAT = "FLOAT"
TOKEN_PLUS = "PLUS"
TOKEN_MINUS = "MINUS"
TOKEN_MULTIPLY = "MULTIPLY"
TOKEN_DIVISION = "DIVISION"
TOKEN_LBRACKET = "LBRACKET"
TOKEN_RBRACKET = "RBRACKET"


class Token:
    def __init__(self, t_type: str, value: any) -> None:
        self.type = t_type
        self.value = value

    def __repr__(self) -> str:
        return f"{self.type}: {self.value}" if self.value else f"{self.type}"
