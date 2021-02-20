from errors.error import Error
from position import Interval


class UnexpectedTokenError(Error):
    def __init__(self, msg: str, interval: Interval) -> None:
        super().__init__("Unexpected Token", msg, interval)
