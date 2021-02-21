from errors.error import Error
from models.context import ExecutionContext
from models.position import Interval, NEW_LINE


class InterpretError(Error):
    context: ExecutionContext

    def __init__(self, msg: str, interval: Interval, context: ExecutionContext):
        super().__init__("Runtime Error", msg, interval)
        self.context = context

    def get_traceback(self) -> str:
        result = ""
        interval = self.interval
        curr_ctx = self.context
        # Determines the number of tabs to prepend
        layer = 1

        while curr_ctx is not None:
            result += "\t" * layer + f"In file {interval.file.name}, at line {str(interval.start.row + 1)}, " \
                                     f"in the context {curr_ctx.name}"
            interval = curr_ctx.parent_interval
            curr_ctx = curr_ctx.parent
            layer += 1

        return "Traceback (most recent call first):" + NEW_LINE + result

    def __str__(self):
        result = super().__str__()
        result += NEW_LINE
        result += self.get_traceback()
        return result
