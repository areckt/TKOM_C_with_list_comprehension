import logging

logging.basicConfig(level=logging.INFO)


class Interpreter:
    def __init__(self, program, visitor):
        self.program = program
        self.visitor = visitor

    def run(self):
        for function in self.program:
            if function.name.name == 'main':
                function.accept(self.visitor)
