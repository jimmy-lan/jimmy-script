from errors.error import Error
from position import Interval


class BadSyntaxError(Error):
    def __init__(self, msg: str, interval: Interval) -> None:
        super().__init__("Bad Syntax", msg, interval)
