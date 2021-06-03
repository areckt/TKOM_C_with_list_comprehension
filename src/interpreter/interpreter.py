import logging

logging.basicConfig(level=logging.INFO)


class Interpreter:
    def __init__(self, program, visitor):
        self.program = program
        self.visitor = visitor(self.program)

    def run(self):
        for function in self.program:
            if function.name.name == 'main':
                # logging.info(function)
                function.accept(self.visitor)
