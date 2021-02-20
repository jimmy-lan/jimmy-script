from typing import Tuple, List

from constants import SPACES, DIGITS
from errors.error import Error
from errors.unexpected_token_error import UnexpectedTokenError
from models.position import Position, Interval, File
from models.token import Token, TOKEN_EOF, TOKEN_INT, TOKEN_FLOAT


class Lexer:
    def __init__(self, raw: str, file: File) -> None:
        self.raw = raw
        self.pos = Position(0, 0, 0)
        self.curr = raw[0] if len(raw) > 0 else None
        self.file = file

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
            token_interval = Interval.from_position(self.pos, self.file)

            if self.curr in SPACES:
                # Ignore, go to the next token
                self.next()
            elif self.curr in DIGITS:
                tokens.append(self.get_number())
            elif Token.is_op_char(self.curr):
                token_type = Token.map_char_to_type(self.curr)
                tokens.append(Token(token_type, interval=token_interval))
                self.next()
            else:
                self.next()
                return [], UnexpectedTokenError(
                    f"Unexpected token '{self.curr}'.",
                    token_interval
                )

        tokens.append(Token(TOKEN_EOF, interval=Interval.from_position(self.pos, self.file)))
        return tokens, None

    def get_number(self) -> Token:
        parsed_str = ""
        num_dots = 0
        start_pos = self.pos.copy()

        while self.curr is not None and self.curr in DIGITS + ".":
            if self.curr == ".":
                if num_dots > 0:
                    break
                num_dots += 1
            parsed_str += self.curr
            self.next()

        # This end position is off-by-one. But it does not matter a lot
        # so I leave it as-is.
        end_pos = self.pos.copy()
        interval = Interval(start_pos, end_pos, self.file)

        if num_dots == 0:
            return Token(TOKEN_INT, int(parsed_str), interval)
        else:
            return Token(TOKEN_FLOAT, float(parsed_str), interval)
