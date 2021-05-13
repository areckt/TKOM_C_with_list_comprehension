from src.lexer.token import TokenType


class ParserUtils:
    type_tokens = [TokenType.INT_KEYWORD, TokenType.FLOAT_KEYWORD, TokenType.STRING_KEYWORD]

    list_type_tokens = [TokenType.INT_LIST_KEYWORD, TokenType.FLOAT_LIST_KEYWORD, TokenType.STRING_LIST_KEYWORD]

    literal_tokens = [TokenType.INT_LITERAL, TokenType.FLOAT_LITERAL, TokenType.STRING_LITERAL]

    multiplicative_operator_tokens = [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO]

    additive_operator_tokens = [TokenType.PLUS, TokenType.MINUS]

    comparison_tokens = [TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.GREATER,
                         TokenType.GREATER_OR_EQUAL, TokenType.LESS, TokenType.LESS_OR_EQUAL]
