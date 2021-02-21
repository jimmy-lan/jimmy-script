from models.context import ExecutionContext
from models.position import File
from models.variable_register import VariableRegister
from processors.interpreter import Interpreter
from processors.laxer import Lexer
from processors.parser import Parser


variable_register = VariableRegister()


def execute(raw: str, fn: str):
    # Construct file object
    file = File(fn, raw)

    # Get tokens from laxer
    lexer = Lexer(raw, file)
    tokens, error = lexer.get_tokens()
    if error:
        return None, error

    # Get abstract syntax tree
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    # Interpret AST
    interpreter = Interpreter()
    execution_context = ExecutionContext("main program")
    execution_context.variable_register = variable_register
    result = interpreter.traverse(ast.node, execution_context)

    return result.value, result.error
