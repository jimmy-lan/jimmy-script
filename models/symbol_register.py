
class SymbolRegister:
    # Dictionary mapping name of variable to value
    symbols: dict
    # Parent symbol register. If the symbol in this register
    # is meant to exist in the global level, then parent would be
    # None. If the symbol register stores values in a function
    # or some other context, then the parent would be another symbol
    # table.
    parent: any

    def __init__(self):
        self.symbols = {}
        self.parent = None
