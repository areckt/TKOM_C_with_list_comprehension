# let GenericError inherit from Exception (which inherits from BaseException)
class GenericError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def fatal(self):
        raise Exception(self.message)

    def warning(self):
        print(self.message)


class LexerError(GenericError):
    def __init__(self, position, message):
        line, column = position
        self.message = f'Lexer error! \n line: {line} column: {column} \n {message}'
        super().__init__(self.message)


class ParserError(GenericError):
    def __init__(self, position, message):
        line, column = position
        self.message = f'Parser error \n line: {line} column: {column} \n {message}'
        super().__init__(self.message)


class ParserSyntaxError(ParserError):
    def __init__(self, position, expected_token, got_token):
        self.message = f'Expected: {expected_token} \n got: {got_token}'
        super(ParserSyntaxError, self).__init__(position, self.message)


class SemanticError(GenericError):
    def __init__(self, message):
        self.message = f'SemanticAnalyzer: {message}'
        super().__init__(self.message)


class SemanticVariableRedeclarationError(SemanticError):
    def __init__(self, var_id):
        self.message = f"redeclaration of variable: {var_id}"
        super().__init__(self.message)


class SemanticInvalidTypeError(SemanticError):
    def __init__(self, expected_type, gotten_type):
        self.message = f"invalid type, expected: {expected_type}, but got {gotten_type}"
        super().__init__(self.message)


class SemanticUnknownSymbolError(SemanticError):
    def __init__(self, gotten_id):
        self.message = f"unknown symbol: {gotten_id}"
        super().__init__(self.message)


class SemanticAssignmentWithoutDeclarationError(SemanticError):
    def __init__(self, gotten_id):
        self.message = f"variable assignment without previous declaration: {gotten_id}"
        super().__init__(self.message)


class SemanticNotNumberInArithmeticExprError(SemanticError):
    def __init__(self, gotten_type):
        self.message = f"invalid type in arithmetic expression: {gotten_type}"
        super().__init__(self.message)


class SemanticReturnNotInsideFunctionBodyError(SemanticError):
    def __init__(self):
        self.message = f"return statement not inside function body"
        super().__init__(self.message)


class SemanticNoSuchFunctionError(SemanticError):
    def __init__(self, fun_name):
        self.message = f"no function named {fun_name}"
        super().__init__(self.message)


class SemanticInvalidNumberOfArgsError(SemanticError):
    def __init__(self, got, expected):
        self.message = f"invalid number of args: expected {got}, but got {expected}"
        super().__init__(self.message)


class SemanticTypesOfArgsInFunInvocationError(SemanticError):
    def __init__(self, fun_name, got, expected):
        self.message = f"invalid types of args in function({fun_name})\n\texpected {expected}, but got {got}"
        super().__init__(self.message)


class SemanticNoReturnExpressionInFunBodyError(SemanticError):
    def __init__(self, fun_name, ):
        self.message = f"no return statement in function - {fun_name}"
        super().__init__(self.message)
