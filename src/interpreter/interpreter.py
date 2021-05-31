import logging

logging.basicConfig(level=logging.INFO)


class Interpreter:
    def __init__(self, parser, visitor):
        self.parser = parser
        self.visitor = visitor

    def run(self):
        program = self.parser.parse_program()
        self.visitor.set_functions_def(program)
        for function in program:
            if function.name.name == 'main':
                logging.info(function)
                function.accept(self.visitor)
