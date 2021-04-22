# let GenericError inherit from Exception (which inherits from BaseException)
class GenericError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def fatal(self):
        print(self.message)
        exit()

    def warning(self):
        print(self.message)


# let LexerError inherit from GenericError
class LexerError(GenericError):
    def __init__(self, position, message):
        line, column = position
        self.message = f'Lexer error! \n line: {line} column: {column} \n {message}'
        super().__init__(self.message)
