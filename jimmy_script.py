from position import File
from processors.laxer import Lexer
from processors.parser import Parser


def execute(raw: str, fn: str):
    # Construct file object
    file = File(raw, fn)

    # Get tokens from laxer
    lexer = Lexer(raw, file)
    tokens, error = lexer.get_tokens()
    if error:
        return None, error

    # Get abstract syntax tree
    parser = Parser(tokens)
    ast = parser.parse()

    return ast.node, ast.error
