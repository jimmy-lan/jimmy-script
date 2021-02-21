from models.position import Interval
from utils import arrows_under_string


class Error:
    # Name of the error
    name: str
    # Error message
    msg: str
    # The interval of characters triggering this error
    interval: Interval

    def __init__(self, name: str, msg: str, interval: Interval) -> None:
        self.name = name
        self.msg = msg
        self.interval = interval

    def __str__(self) -> str:
        return f"{self.name}: " \
               f"\n\t{self.msg}" \
               f"\nAt Line {self.interval.start.row + 1} in File {self.interval.file.name}.\n\n" \
               f">>> {arrows_under_string(self.interval.file.content, self.interval, 4)}\n"
