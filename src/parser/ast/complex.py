# complex introduce new scope; can contain other complex
from src.parser.ast.primitives import *


class FunctionDeclaration(AstNode):
    def __init__(self, type_token, id_token, arguments, instructions):
        self.type = Type(type_token)
        self.name = Id(id_token)
        self.arguments = arguments
        self.instructions = instructions

    def __repr__(self):
        args = str(self.arguments)
        if len(self.arguments) == 0:
            args = ''

        nested_ins = str(self.instructions)
        if len(self.instructions) == 0:
            nested_ins = ''

        return f'FunDecl: {self.type} {self.name} ({args} {{{nested_ins}}})'

    def accept(self, visitor):
        return visitor.visit_function_declaration(self)


class IfStatement(AstNode):
    def __init__(self, condition, if_instructions, else_instructions):
        self.condition = condition
        self.if_instructions = if_instructions
        self.else_instructions = else_instructions

    def __repr__(self):
        nested_if_ins = str(self.if_instructions)
        if len(self.if_instructions) == 0:
            nested_if_ins = ''

        nested_else_ins = str(self.else_instructions)
        if len(self.else_instructions) == 0:
            nested_else_ins = ''

        return f'IfStmt: ({self.condition}) {{{nested_if_ins}}} Else: {{{nested_else_ins}}}'

    def accept(self, visitor):
        return visitor.visit_if_statement(self)


class WhileStatement(AstNode):
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions

    def __repr__(self):
        nested_ins = str(self.instructions)
        if len(self.instructions) == 0:
            nested_ins = ''

        return f'WhileStmt: ({self.condition}) {{{nested_ins}}}'

    def accept(self, visitor):
        return visitor.visit_while_statement(self)
