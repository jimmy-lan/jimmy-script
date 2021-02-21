from errors.error import Error
from models.position import Interval


class RuntimeError(Error):
    def __init__(self, msg: str, interval: Interval):
        super().__init__("Runtime Error", msg, interval)
