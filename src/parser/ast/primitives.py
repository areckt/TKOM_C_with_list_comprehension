# primitives - leaves of AST which do not contain other nodes
from src.parser.ast.ast_node import AstNode
from src.parser.ast.ast_utils import *


class ArithmeticOperator(AstNode):
    def __init__(self, token_operator):
        self.type = ArithmeticOperator.get_type_from_token(token_operator)

    @staticmethod
    def get_type_from_token(token_operator):
        token_type = token_operator.get_type()
        if token_type in Dictionaries.token_to_arithmetic_operator:
            return Dictionaries.token_to_arithmetic_operator[token_type]

    def __repr__(self):
        return Dictionaries.primitive_to_string[self.type]


class ComparisonOperator(AstNode):
    def __init__(self, token):
        self.type = ComparisonOperator.get_type_from_token(token)

    @staticmethod
    def get_type_from_token(token_operator):
        token_type = token_operator.get_type()
        if token_type in Dictionaries.token_to_comparison_operator:
            return Dictionaries.token_to_comparison_operator[token_type]

    def __repr__(self):
        return Dictionaries.primitive_to_string[self.type]


class LogicalOperator(AstNode):
    def __init__(self, token):
        self.type = LogicalOperator.get_type_from_token(token)

    @staticmethod
    def get_type_from_token(token_operator):
        token_type = token_operator.get_type()
        if token_type in Dictionaries.token_to_logical_operator:
            return Dictionaries.token_to_logical_operator[token_type]

    def __repr__(self):
        return Dictionaries.primitive_to_string[self.type]


class Id(AstNode):
    def __init__(self, id_token, is_reversed=False, calculate_len=False):
        if TokenType.IDENTIFIER == id_token.get_type():
            self.name = id_token.get_value()
            self.reversed = is_reversed
            self.len = calculate_len

    def __repr__(self):
        if not self.reversed and not self.len:
            return f'id: {self.name}'
        if self.reversed:
            return f'id: reversed({self.name})'
        if self.len:
            return f'len( id: {self.name} )'


class Type(AstNode):
    def __init__(self, type_token):
        if type_token.get_type() in Dictionaries.token_to_types:
            self.type = Dictionaries.token_to_types[type_token.get_type()]

    def __repr__(self):
        return Dictionaries.primitive_to_string[self.type]
