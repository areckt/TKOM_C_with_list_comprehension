from src.parser.ast.primitives import *
from src.parser.ast.semi_complex import *
from src.parser.ast.complex import *
from src.lexer.source import *
from src.lexer.token import *
from .exceptions import *
from src.interpreter.visitor_utils import *
import operator


class Visitor:
    def __init__(self, list_of_instructions):
        self.list_of_instructions = list_of_instructions
        self.var_symbols = {}
        self.fun_symbols = {}

    # ########### #
    #  U T I L S  #
    # ########### #

    def get_variable_value(self, variable_name):
        return self.var_symbols[variable_name].get_value

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

    @staticmethod
    def calculate_numeric_expression(left_operand, right_operand, operation):
        if (isinstance(left_operand, int) and isinstance(right_operand, int)) or \
                (isinstance(left_operand, float) and isinstance(right_operand, float)):
            if operation == '+':
                return left_operand + right_operand
            elif operation == '-':
                return left_operand - right_operand
            elif operation == '*':
                return left_operand * right_operand
            elif operation == '/':
                if right_operand == 0:
                    raise DivisionError()
                return left_operand / right_operand
            else:
                raise UndefinedOperation(type(left_operand).__name__, operation, type(right_operand).__name__)

    # ##################### #
    #  P R I M I T I V E S  #
    # ##################### #

    def visit_arithmetic_operator(self, node):
        return str(node.type)

    def visit_comparison_operator(self, node):
        return str(node.type)

    def visit_logical_operator(self, node):
        return str(node.type)

    @staticmethod
    def visit_id(node):
        return node.name

    def visit_type(self, node):
        return str(node.type)

    # ######################## #
    #  S E M I - C O M P L E X #
    # ######################## #

    def visit_literal(self, node):
        return node.get_value()

    def visit_unary_operation(self, node):
        pass

    def visit_list_element(self, node):
        list_name = node.name.name
        list_value = self.var_symbols[list_name].get_value
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

    def visit_function_argument(self, node):
        return node.name.name

    def visit_function_invocation(self, node):
        pass

    def visit_single_condition(self, node):
        pass

    def visit_arithmetic_expression(self, node):
        left_operand = node.left_operand.accept(self)
        operation = node.operator.accept(self)
        right_operand = node.right_operand.accept(self)

        assign_value = self.try_variable_assign(operation, left_operand, right_operand)
        if assign_value is not None:
            return assign_value

        if isinstance(left_operand, str):
            left_operand = self.get_variable_value(left_operand)
        if isinstance(right_operand, str):
            right_operand = self.get_variable_value(right_operand)

        return_value = self.calculate_numeric_expression(left_operand, right_operand, operation)
        if return_value is None:
            raise UndefinedOperation(type(left_operand).__name__, operation. type(right_operand).__name__)
        return return_value

    def visit_return_expression(self, node):
        return_value = self.evaluate_node_value(node.value)
        print(return_value)
        return return_value

    # COMPLEX
    def visit_function_declaration(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

    def visit_if_statement(self, node):
        pass

    def visit_while_statement(self, node):
        pass
