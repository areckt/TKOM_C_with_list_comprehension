# let GenericError inherit from Exception (which inherits from BaseException)
class GenericError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def fatal(self):
        print(self.message)
        exit(-1)

    def warning(self):
        print(self.message)


# let LexerError inherit from GenericError
class LexerError(GenericError):
    def __init__(self, position, message):
        line, column = position
        self.message = f'Lexer error! \n line: {line} column: {column} \n {message}'
        super().__init__(self.message)


# handling Parser errors
class ParserError(GenericError):
    def __init__(self, position, message):
        line, column = position
        self.message = f'Parser error \n line: {line} column: {column} \n {message}'
        super().__init__(self.message)


class ParserSyntaxError(ParserError):
    def __init__(self, position, expected_token, got_token):
        self.message = f'Expected: {expected_token} \n got: {got_token}'
        super(ParserSyntaxError, self).__init__(position, self.message)
