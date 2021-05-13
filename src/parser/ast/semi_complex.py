# semi_complex - they consist of primitives and other semi_complex but do not introduce new scope
from src.parser.ast.primitives import *


class Literal(AstNode):
    def __init__(self, literal_token):
        self.type, self.value = Literal.init_literal(literal_token)

    def __repr__(self):
        return f'literal: {self.value}'

    def get_value(self):
        return self.value

    @staticmethod
    def init_literal(literal_token):
        literal_type = literal_token.get_type()
        value = literal_token.get_value()
        if literal_type == TokenType.INT_LITERAL and isinstance(value, int):
            return Type(Token(TokenType.INT_KEYWORD)), value
        elif literal_type == TokenType.FLOAT_LITERAL and isinstance(value, float):
            return Type(Token(TokenType.FLOAT_KEYWORD)), value
        elif literal_type == TokenType.STRING_LITERAL and isinstance(value, str):
            return Type(Token(TokenType.STRING_KEYWORD)), value


class ListElement(AstNode):
    def __init__(self, id_token, index, is_reversed=False, calculate_len=False):
        self.name = id_token
        self.index = index
        self.reversed = is_reversed
        self.len = calculate_len

    def __repr__(self):
        if not self.reversed and not self.len:
            return f'ListElement: {self.name}[{self.index}]'
        if self.reversed:
            return f'ListElement: reversed({self.name}[{self.index}])'
        if self.len:
            return f'len( ListElement: {self.name}[{self.index}] )'


class VariableDeclaration(AstNode):
    def __init__(self, type_token, id_token, value):
        self.type = Type(type_token)
        self.name = Id(id_token)
        self.value = value

    def __repr__(self):
        return f'VarDecl: {self.type} {self.name} = {self.value};'


class ListVariableDeclaration(AstNode):
    def __init__(self, type_token, id_token, values):
        self.type = Type(type_token)
        self.name = Id(id_token)
        self.values = values

    def __repr__(self):
        values_str = str(self.values)
        if len(self.values) == 0:
            values_str = ''
        return f'ListVarDecl: {self.name} = values: {values_str}'


class ListComprehensionDeclaration(AstNode):
    def __init__(self, type_token, id_token, what_expression, for_id, in_expression):
        self.type = Type(type_token)
        self.name = Id(id_token)
        self.what_expression = what_expression
        self.for_id = for_id
        self.in_expression = in_expression

    def __repr__(self):
        return f'ListCmprhnsnDecl: {self.name} = [{self.what_expression} for {self.for_id} in {self.in_expression}]'


class VariableAssignment(AstNode):
    def __init__(self, id_token, value):
        self.name = Id(id_token)
        self.value = value

    def __repr__(self):
        return f'VarAssign: {self.name} = {self.value};'


class ListVariableAssignment(AstNode):
    def __init__(self, id_token, values):
        self.name = Id(id_token)
        self.values = values

    def __repr__(self):
        values_str = str(self.values)
        if len(self.values) == 0:
            values_str = ''
        return f'ListVarAssign: {self.name} = values: {values_str}'


class ListComprehensionAssignment(AstNode):
    def __init__(self, id_token, what_expression, for_id, in_expression):
        self.name = Id(id_token)
        self.what_expression = what_expression
        self.for_id = for_id
        self.in_expression = in_expression

    def __repr__(self):
        return f'ListCmprhnsnAssign: {self.name} = [{self.what_expression} for {self.for_id} in {self.in_expression}]'


class FunctionArgument(AstNode):
    def __init__(self, type_token, id_token):
        self.type = Type(type_token)
        self.name = Id(id_token)

    def __repr__(self):
        return f'FuncArg: ({self.type}-{self.name})'


class FunctionInvocation(AstNode):
    def __init__(self, id_token, arguments):
        self.name = Id(id_token)
        self.arguments = arguments

    def __repr__(self):
        arg_str = str(self.arguments)
        if len(self.arguments) == 0:
            arg_str = ''
        return f'FuncInvoc: {self.name} ({arg_str})'


class SingleCondition(AstNode):
    def __init__(self, left, operator_token=None, right=None):
        self.left = left
        self.operator = None
        self.right = None
        if operator_token:
            self.operator = ComparisonOperator(operator_token)
            self.right = right

    def __repr__(self):
        return f'SingleCond: ({self.left}{self.operator}{self.right})'


class ArithmeticExpression(AstNode):
    def __init__(self, left_operand, operator, right_operand):
        self.left_operand = left_operand
        self.operator = operator
        self.right_operand = right_operand

    def __repr__(self):
        return f'ArithmExpr: ({self.left_operand}{self.operator}{self.right_operand})'


class ReturnExpression(AstNode):
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return_value = ''
        if self.value is not None:
            return_value = str(self.value)
        return f'Return: {return_value};'
