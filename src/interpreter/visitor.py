import copy

from src.parser.ast.primitives import *
from src.parser.ast.semi_complex import *
from src.parser.ast.complex import *
from src.lexer.source import *
from src.lexer.token import *
from .exceptions import *
from src.interpreter.visitor_utils import *
import operator


class Visitor:
    def __init__(self):
        self.var_symbols = {}
        self.fun_symbols = {}
        self.was_return = False

    # ########### #
    #  U T I L S  #
    # ########### #

    def get_variable_value(self, variable_name):
        return self.var_symbols[variable_name].get_value()

    def set_variable_value(self, variable_name, new_value):
        self.var_symbols[variable_name].set_value(new_value)

    def find_function_def(self, identifier, arguments_num):
        for function_def in self.fun_symbols:
            if function_def.identifier == identifier and len(function_def.arguments) == arguments_num:
                return function_def

    def save_variable(self, variable_name, variable_value):
        self.var_symbols[variable_name] = Variable(variable_name, variable_value)

    def evaluate_node_value(self, node):
        if isinstance(node, Literal):
            return node.get_value()
        elif isinstance(node, Id):
            return self.get_variable_value(node.name)
        elif isinstance(node, ArithmeticExpression):
            return self.visit_arithmetic_expression(node)
        elif isinstance(node, ListElement):
            return self.visit_list_element(node)
        elif isinstance(node, UnaryOperation):
            return self.visit_unary_operation(node)

    # def does_element_meet_conditions(self, element, conditions):
    #     operators = {
    #         '>': operator.gt,
    #         '<': operator.lt,
    #         '>=': operator.ge,
    #         '<=': operator.le,
    #         '==': operator.eq,
    #         '!=': operator.ne
    #     }
    #     for condition in conditions:
    #         operation, expression = condition.accept(self)
    #         operation = operators[operation]
    #         if not (operation(element, expression)):
    #             return False
    #     return True

    # ##################### #
    #  P R I M I T I V E S  #
    # ##################### #

    @staticmethod
    def visit_arithmetic_operator(node):
        if node.type == ArithmeticOperatorTypes.PLUS:
            return "+"
        elif node.type == ArithmeticOperatorTypes.MINUS:
            return "-"
        elif node.type == ArithmeticOperatorTypes.MULTIPLY:
            return "*"
        elif node.type == ArithmeticOperatorTypes.DIVIDE:
            return "/"
        elif node.type == ArithmeticOperatorTypes.MODULO:
            return "%"
        elif node.type == ArithmeticOperatorTypes.LENGTH_OP:
            return "_"
        elif node.type == ArithmeticOperatorTypes.NOT:
            return "!"

    @staticmethod
    def visit_comparison_operator(node):
        if node.type == ComparisonOperatorTypes.LESS:
            return "<"
        elif node.type == ComparisonOperatorTypes.LESS_OR_EQUAL:
            return "<="
        elif node.type == ComparisonOperatorTypes.EQUAL:
            return "=="
        elif node.type == ComparisonOperatorTypes.NOT_EQUAL:
            return "!="
        elif node.type == ComparisonOperatorTypes.GREATER:
            return ">"
        elif node.type == ComparisonOperatorTypes.GREATER_OR_EQUAL:
            return ">="

    @staticmethod
    def visit_logical_operator(node):
        if node.type == LogicalOperatorTypes.NOT:
            return "!"
        elif node.type == LogicalOperatorTypes.OR:
            return "||"
        elif node.type == LogicalOperatorTypes.AND:
            return "&&"

    @staticmethod
    def visit_id(node):
        return node.name

    @staticmethod
    def visit_type(node):
        return str(node.type)

    # ######################### #
    #  S E M I - C O M P L E X  #
    # ######################### #

    @staticmethod
    def visit_literal(node):
        return node.get_value()

    def visit_unary_operation(self, node):
        unary_operator = node.unary_operator
        unary_operator = self.visit_arithmetic_operator(unary_operator)

        expression = node.expression
        expression = self.evaluate_node_value(expression)

        result = None

        if unary_operator == "-":
            result = expression * (-1)
        elif unary_operator == "!":
            result = expression
            result.reverse()
        elif unary_operator == "_":
            result = len(expression)

        return result

    def visit_list_element(self, node):
        list_name = node.name.name
        list_value = self.var_symbols[list_name].get_value()
        list_length = len(list_value)
        index = node.index

        index = self.evaluate_node_value(index)

        if list_length > index >= 0:
            return list_value[index]
        else:
            raise IndexOutOfRange()

    def visit_variable_declaration(self, node):
        var_name = node.name.name
        var_value = node.value

        var_value = self.evaluate_node_value(var_value)

        self.save_variable(var_name, var_value)

    def visit_list_variable_declaration(self, node):
        var_name = node.name.name
        var_values = node.values
        final_values = []
        for value in var_values:
            final_values.append(self.evaluate_node_value(value))

        self.save_variable(var_name, final_values)

    def visit_list_comprehension_declaration(self, node):
        pass

    def visit_variable_assignment(self, node):
        var_name = node.name.name
        new_value = self.evaluate_node_value(node.value)
        self.set_variable_value(var_name, new_value)

    def visit_list_variable_assignment(self, node):
        var_name = node.name.name
        new_values = node.values
        target_values = []
        for new_value in new_values:
            target_values.append(self.evaluate_node_value(new_value))
        self.set_variable_value(var_name, target_values)

    def visit_list_comprehension_assignment(self, node):
        pass

    @staticmethod
    def visit_function_argument(node):
        return node.name.name

    def visit_function_invocation(self, node):
        pass

    def visit_single_condition(self, node):
        left = node.left
        left = self.evaluate_node_value(left)

        right = node.right
        right = self.evaluate_node_value(right)

        comparison_operator = node.operator
        comparison_operator = self.visit_comparison_operator(comparison_operator)

        result = None

        if comparison_operator == "<":
            result = left < right
        elif comparison_operator == "<=":
            result = left <= right
        elif comparison_operator == "==":
            result = left == right
        elif comparison_operator == "!=":
            result = left != right
        elif comparison_operator == ">":
            result = left > right
        elif comparison_operator == ">=":
            result = left >= right

        return result

    def visit_arithmetic_expression(self, node):
        left_operand = node.left_operand
        left_operand = self.evaluate_node_value(left_operand)

        right_operand = node.right_operand
        right_operand = self.evaluate_node_value(right_operand)

        operator_symbol = node.operator
        operator_symbol = self.visit_arithmetic_operator(operator_symbol)

        result = None

        if operator_symbol == "+":
            result = left_operand + right_operand
        elif operator_symbol == "-":
            result = left_operand - right_operand
        elif operator_symbol == "*":
            result = left_operand * right_operand
        elif operator_symbol == "/":
            if right_operand == 0:
                raise DivisionError()
            else:
                result = left_operand / right_operand

        return result

    def visit_return_expression(self, node):
        return_value = self.evaluate_node_value(node.value)
        print("RETURN: " + str(return_value))
        self.was_return = True
        return return_value

    # ############### #
    #  C O M P L E X  #
    # ############### #

    def visit_function_declaration(self, node):
        for instruction in node.instructions:
            if not self.was_return:
                instruction.accept(self)

    def visit_if_statement(self, node):
        condition = node.condition
        condition = self.visit_single_condition(condition)

        if_instructions = node.if_instructions
        else_instructions = node.else_instructions

        if condition:
            for instruction in if_instructions:
                if not self.was_return:
                    instruction.accept(self)
        else:
            if else_instructions != '':
                for instruction in else_instructions:
                    if not self.was_return:
                        instruction.accept(self)

    def visit_while_statement(self, node):
        condition = node.condition
        condition = self.visit_single_condition(condition)

        instructions = node.instructions

        if condition:
            while condition:
                for instruction in instructions:
                    if not self.was_return:
                        instruction.accept(self)
                condition = self.visit_single_condition(node.condition)
