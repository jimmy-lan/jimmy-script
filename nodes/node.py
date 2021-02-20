from token import Token


class Node:
    def __init__(self, token: Token):
        self.token = token

    def __repr__(self):
        return str(self.token)
