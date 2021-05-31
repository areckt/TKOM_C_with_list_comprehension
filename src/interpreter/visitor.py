from ..parser.ast.primitives import *
from ..parser.ast.semi_complex import *
from ..parser.ast.complex import *
from ..lexer.source import *
from ..lexer.token import *


class Visitor():
    # PRIMITIVES
    def visit_ArithmeticOperator(self, node):
        pass

    def visit_ComparisonOperator(self, node):
        pass

    def visit_LogicalOperator(self, node):
        pass

    def visit_Id(self, node):
        pass

    def visit_Type(self, node):
        pass

    # SEMI-COMPLEX
    def visit_Literal(self, node):
        pass

    def visit_UnaryOperation(self, node):
        pass

    def visit_ListElement(self, node):
        pass

    def visit_VariableDeclaration(self, node):
        pass

    def visit_ListVariableDeclaration(self, node):
        pass

    def visit_ListComprehensionDeclaration(self, node):
        pass

    def visit_VariableAssignment(self, node):
        pass

    def visit_ListVariableAssignment(self, node):
        pass

    def visit_ListComprehensionAssignment(self, node):
        pass

    def visit_FunctionArgument(self, node):
        pass

    def visit_FunctionInvocation(self, node):
        pass

    def visit_SingleCondition(self, node):
        pass

    def visit_ArithmeticExpression(self, node):
        pass

    def visit_ReturnExpression(self, node):
        pass

    def visit_FunctionDeclaration(self, node):
        pass

    def visit_IfStatement(self, node):
        pass

    def visit_WhileStatement(self, node):
        pass
