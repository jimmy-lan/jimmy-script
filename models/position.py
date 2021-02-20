from typing import Optional

from constants import *


class File:
    # Name of the file, use <stdin> for shell executions
    name: str
    # Content in the file, use the character '\n' for newline
    content: str

    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content


class Position:
    """
    Represent a position of a character in a file.
    """
    # The index of the character, in the context of the entire file.
    idx: int
    # The row that the character can be found in. Row number starts
    # from 0.
    row: int
    # The column that the character can be found in. Column number
    # starts from 0.
    col: int

    def __init__(self, idx: int, row: int, col: int) -> None:
        self.idx = idx
        self.row = row
        self.col = col

    def next(self, curr: str = None):
        self.idx += 1

        if curr == NEW_LINE:
            self.row += 1
            self.col = 0
        else:
            self.col += 1

        return self

    def copy(self):
        return Position(self.idx, self.row, self.col)


class Interval:
    """
    Represent an interval containing a starting position and an ending
    position in a file.
    """
    # Starting position of the interval
    start: Position
    # Ending position of the interval
    end: Position
    # File that this interval resides in
    file: File

    @staticmethod
    def from_position(pos: Position, file: Optional[File]):
        return Interval(pos, pos, file)

    def __init__(self, start: Position, end: Position, file: Optional[File]):
        self.start = start
        self.end = end
        self.file = file
