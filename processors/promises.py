from errors.error import Error
from nodes.node import Node


class Promise:
    def resolve(self, data: any):
        raise NotImplementedError()

    def reject(self, error: any):
        raise NotImplementedError()


class ParserPromise(Promise):
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, promise):
        if isinstance(promise, ParserPromise):
            if promise.error is not None:
                self.error = promise.error
            return promise.node
        return promise

    def resolve(self, node: Node):
        self.node = node
        return self

    def reject(self, error: Error):
        self.error = error
        return self


class InterpreterPromise(Promise):
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, promise):
        if promise.error:
            self.error = promise.error
        return promise.value

    def resolve(self, value):
        self.value = value
        return self.value

    def reject(self, error):
        self.error = error
        return self.error
