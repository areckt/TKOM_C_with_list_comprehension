from enum import Enum, auto, unique


@unique
class TokenType(Enum):

    # general
    EOF_SYMBOL = auto()             # EOF
    IDENTIFIER = auto()             # identifier
    SEMICOLON = auto()              # ";"
    COMMA = auto()                  # ","

    # brackets
    OPEN_BRACKET = auto()           # "("
    CLOSE_BRACKET = auto()          # ")"
    OPEN_BLOCK = auto()             # "{"
    CLOSE_BLOCK = auto()            # "}"
    OPEN_LIST = auto()              # "["
    CLOSE_LIST = auto()             # "]"

    # arithmetic operators
    PLUS = auto()                   # "+"
    MINUS = auto()                  # "-"
    MULTIPLY = auto()               # "*"
    DIVIDE = auto()                 # "/"
    MODULO = auto()                 # "%"
    LENGTH_OP = auto()              # "_"

    # logical and bool operators
    AND = auto()                    # "&&"
    OR = auto()                     # "||"
    NOT = auto()                    # "!"
    LESS = auto()                   # "<"
    LESS_OR_EQUAL = auto()          # "<="
    EQUAL = auto()                  # "=="
    NOT_EQUAL = auto()              # "!="
    GREATER = auto()                # ">"
    GREATER_OR_EQUAL = auto()       # ">="

    # assign operator
    ASSIGN = auto()                 # "="

    # literals
    INT_LITERAL = auto()            # e.g. 5
    FLOAT_LITERAL = auto()          # e.g. 4.5
    STRING_LITERAL = auto()         # e.g. 'great'

    # keywords
    RETURN_KEYWORD = auto()         # 'return'
    WHILE_KEYWORD = auto()          # 'while'
    IF_KEYWORD = auto()             # 'for'
    ELSE_KEYWORD = auto()           # 'else'
    FOR_KEYWORD = auto()            # 'for'
    IN_KEYWORD = auto()             # 'in'
    INT_KEYWORD = auto()            # 'int'
    INT_LIST_KEYWORD = auto()       # 'int[]'
    FLOAT_KEYWORD = auto()          # 'float'
    FLOAT_LIST_KEYWORD = auto()     # 'float[]'
    STRING_KEYWORD = auto()         # 'string'
    STRING_LIST_KEYWORD = auto()    # 'string[]'

    UNKNOWN = auto()


class Token:
    def __init__(self, token_type: TokenType, value="", line: int = 0, column: int = 0):
        self.type = token_type
        self.line = line
        self.column = column
        self.value = value

    def get_position(self):
        # returns (line, column)
        return self.line, self.column

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value

    # string representation of an object
    # used for debugging
    def __repr__(self):
        rep = str(self.type.name).ljust(26) + str(self.value).ljust(26) + \
              "line: " + str(self.line) + str(" ,") + str(self.column)
        # rep = f'{self.type.name} \t {self.value} \t pos({self.line}, {self.column})'
        return rep


class TokenDicts:
    keywords = {
        'return': TokenType.RETURN_KEYWORD,
        'while': TokenType.WHILE_KEYWORD,
        'if': TokenType.IF_KEYWORD,
        'else': TokenType.ELSE_KEYWORD,
        'for': TokenType.FOR_KEYWORD,
        'in': TokenType.IN_KEYWORD,
        'int': TokenType.INT_KEYWORD,
        'int[]': TokenType.INT_LIST_KEYWORD,
        'float': TokenType.FLOAT_KEYWORD,
        'float[]': TokenType.FLOAT_LIST_KEYWORD,
        'string': TokenType.STRING_KEYWORD,
        'string[]': TokenType.STRING_LIST_KEYWORD
    }

    one_char_tokens = {
        ';': TokenType.SEMICOLON,
        ',': TokenType.COMMA,
        '(': TokenType.OPEN_BRACKET,
        ')': TokenType.CLOSE_BRACKET,
        '{': TokenType.OPEN_BLOCK,
        '}': TokenType.CLOSE_BLOCK,
        '[': TokenType.OPEN_LIST,
        ']': TokenType.CLOSE_LIST,
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.MULTIPLY,
        '/': TokenType.DIVIDE,
        '%': TokenType.MODULO,
        '!': TokenType.NOT,
        '<': TokenType.LESS,
        '>': TokenType.GREATER,
        '=': TokenType.ASSIGN,
        '_': TokenType.LENGTH_OP
    }

    two_char_tokens = {
        '&&':       TokenType.AND,
        '||':       TokenType.OR,
        '<=':       TokenType.LESS_OR_EQUAL,
        '==':       TokenType.EQUAL,
        '!=':       TokenType.NOT_EQUAL,
        '>=':       TokenType.GREATER_OR_EQUAL
    }
