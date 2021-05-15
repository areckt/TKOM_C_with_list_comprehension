from enum import Enum, auto, unique
from src.lexer.token import TokenType, Token


@unique
class Types(Enum):
    INT = auto()
    FLOAT = auto()
    STRING = auto()


@unique
class ListTypes(Enum):
    LINT = auto()
    LFLOAT = auto()
    LSTRING = auto()


@unique
class ArithmeticOperatorTypes(Enum):
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    NOT = auto()
    LENGTH = auto()


@unique
class ComparisonOperatorTypes(Enum):
    EQUAL = auto()
    NOT_EQUAL = auto()
    GREATER = auto()
    GREATER_OR_EQUAL = auto()
    LESS = auto()
    LESS_OR_EQUAL = auto()


@unique
class LogicalOperatorTypes(Enum):
    NOT = auto()
    OR = auto()
    AND = auto()


class Dictionaries:
    token_to_types = {
        TokenType.INT_KEYWORD: Types.INT,
        TokenType.FLOAT_KEYWORD: Types.FLOAT,
        TokenType.STRING_KEYWORD: Types.STRING,
        TokenType.INT_LIST_KEYWORD: ListTypes.LINT,
        TokenType.FLOAT_LIST_KEYWORD: ListTypes.LFLOAT,
        TokenType.STRING_LIST_KEYWORD: ListTypes.LSTRING,
    }

    token_to_arithmetic_operator = {
        TokenType.PLUS: ArithmeticOperatorTypes.PLUS,
        TokenType.MINUS: ArithmeticOperatorTypes.MINUS,
        TokenType.MULTIPLY: ArithmeticOperatorTypes.MULTIPLY,
        TokenType.DIVIDE: ArithmeticOperatorTypes.DIVIDE,
        TokenType.MODULO: ArithmeticOperatorTypes.MODULO,
        TokenType.NOT: ArithmeticOperatorTypes.NOT,
        TokenType.LENGTH_OP: ArithmeticOperatorTypes.LENGTH
    }

    token_to_comparison_operator = {
        TokenType.EQUAL: ComparisonOperatorTypes.EQUAL,
        TokenType.NOT_EQUAL: ComparisonOperatorTypes.NOT_EQUAL,
        TokenType.GREATER: ComparisonOperatorTypes.GREATER,
        TokenType.GREATER_OR_EQUAL: ComparisonOperatorTypes.GREATER_OR_EQUAL,
        TokenType.LESS: ComparisonOperatorTypes.LESS,
        TokenType.LESS_OR_EQUAL: ComparisonOperatorTypes.LESS_OR_EQUAL
    }

    token_to_logical_operator = {
        TokenType.NOT: LogicalOperatorTypes.NOT,
        TokenType.OR: LogicalOperatorTypes.OR,
        TokenType.AND: LogicalOperatorTypes.AND
    }

    primitive_to_string = {
        ArithmeticOperatorTypes.PLUS: '+',
        ArithmeticOperatorTypes.MINUS: '-',
        ArithmeticOperatorTypes.MULTIPLY: '*',
        ArithmeticOperatorTypes.DIVIDE: '/',
        ArithmeticOperatorTypes.MODULO: '%',

        ComparisonOperatorTypes.EQUAL: '==',
        ComparisonOperatorTypes.NOT_EQUAL: '!=',
        ComparisonOperatorTypes.GREATER: '>',
        ComparisonOperatorTypes.GREATER_OR_EQUAL: '>=',
        ComparisonOperatorTypes.LESS: '<',
        ComparisonOperatorTypes.LESS_OR_EQUAL: '<=',

        LogicalOperatorTypes.NOT: '!',
        LogicalOperatorTypes.OR: '||',
        LogicalOperatorTypes.AND: '&&',

        Types.INT: 'int',
        Types.FLOAT: 'float',
        Types.STRING: 'string',

        ListTypes.LINT: 'lint',
        ListTypes.LFLOAT: 'lfloat',
        ListTypes.LSTRING: 'lstring'
    }
