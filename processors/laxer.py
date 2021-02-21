from typing import Tuple, List

from errors.error import Error
from errors.unexpected_token_error import UnexpectedTokenError
from models.position import *
from models.token import *


class Lexer:
    """
    A laxer takes in a raw piece of code (it can be single line or
    multi-line) and breaks it down to an array of tokens.
    """
    # The raw text to process
    raw: str
    # Current processing position
    pos: Position
    # Current processing character
    curr: str or None
    # File context
    file: File

    def __init__(self, raw: str, file: File) -> None:
        self.raw = raw
        self.pos = Position(0, 0, 0)
        self.curr = raw[0] if len(raw) > 0 else None
        self.file = file

    def next(self) -> None:
        """ Move on to the next character. """
        self.pos.next(self.curr)
        idx = self.pos.idx
        if idx < len(self.raw):
            self.curr = self.raw[idx]
        else:
            self.curr = None

    def revert(self, pos: Position) -> None:
        """ Revert to a character position. """
        self.pos = pos
        self.curr = self.raw[self.pos.idx]

    def get_tokens(self) -> Tuple[List[Token], Error or None]:
        tokens = []

        while self.curr is not None:
            token_interval = Interval.from_position(self.pos, self.file)

            if self.curr in SPACES:
                # Ignore, go to the next token
                self.next()
                continue
            # The order of this if statement is important
            if self.curr in ASSIGNMENT_OP_CHAR:
                token = self.get_assignment()
                # If token is none, we revert position and continue to
                # cases below to see if there is a match.
                if token is not None:
                    tokens.append(token)
                    continue
            if self.curr in DIGITS:
                tokens.append(self.get_number())
                continue
            if self.curr in LETTERS:
                tokens.append(self.get_identifier())
                continue
            if Token.is_op_char(self.curr):
                token_type = Token.map_char_to_type(self.curr)
                tokens.append(Token(token_type, interval=token_interval))
                self.next()
                continue

            # Unexpected character
            unexpected_token = self.curr
            self.next()
            return [], UnexpectedTokenError(
                f"Unexpected token '{unexpected_token}'.",
                token_interval
            )

        tokens.append(Token(TOKEN_EOF, interval=Interval.from_position(self.pos, self.file)))
        return tokens, None

    def get_identifier(self) -> Token:
        parsed_str = ""
        start_pos = self.pos.copy()

        while self.curr is not None and self.curr in IDENTIFIER_CHAR:
            parsed_str += self.curr
            self.next()

        # Keywords in Jimmy Script will not be case sensitive
        parsed_str = parsed_str.lower()
        if parsed_str in KEYWORDS:
            token_type = TOKEN_KEYWORD
        else:
            token_type = TOKEN_IDENTIFIER

        end_pos = self.pos.copy()
        interval = Interval(start_pos, end_pos, self.file)
        return Token(token_type, parsed_str, interval)

    def get_assignment(self) -> Token or None:
        parsed_str = ""
        start_pos = self.pos.copy()

        while self.curr is not None and self.curr in ASSIGNMENT_OP_CHAR:
            parsed_str += self.curr
            self.next()

        if parsed_str in ASSIGNMENT_OP:
            end_pos = self.pos.copy()
            interval = Interval(start_pos, end_pos, self.file)
            return Token(TOKEN_ASSIGNMENT, parsed_str, interval)
        else:
            return self.revert(start_pos)

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
