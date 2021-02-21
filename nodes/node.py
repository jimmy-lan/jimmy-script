from models.token import Token


class Node:
    def __init__(self, token: Token):
        self.token = token
        self.interval = self.token.interval

    def __repr__(self):
        return str(self.token)
