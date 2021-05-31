from ..lexer.lexer import Lexer
from ..lexer.source import Source
from ..parser.parser import Parser
from .visitor import Visitor


class Interpreter:
    def __init__(self, parser, visitor):
        self.parser = parser
        self.visitor = visitor

    def run(self):
        program = self.parser.parse_program()
        for function in program:
            if function.name.name == 'main':
                print(function)
                function.accept(self.visitor)
