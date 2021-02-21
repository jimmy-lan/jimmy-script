
class VariableRegister:
    # Dictionary mapping name of variable to value
    variables: dict
    # Parent variable register. If the variables in this register
    # is meant to exist in the global level, then parent would be
    # None. If the variable register stores variables in a function
    # or some other context, then the parent would be another variable
    # register.
    parent: any

    def __init__(self):
        self.variables = {}
        self.parent = None

    def get(self, name: str) -> any:
        val = self.variables.get(name, None)
        if val is None and self.parent is not None:
            return self.parent.get
        return val

    def set(self, name: str, val: any) -> None:
        self.variables[name] = val

    def remove(self, name: str):
        del self.variables[name]
