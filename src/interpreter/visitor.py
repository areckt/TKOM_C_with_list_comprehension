from ..parser.ast.primitives import *
from ..parser.ast.semi_complex import *
from ..parser.ast.complex import *
from ..lexer.source import *
from ..lexer.token import *
from .exceptions import *
import operator


class Visitor:
    def __init__(self):
        self.map = []
        self.functions_def = []
        self.map.append({})

    def get_map(self):
        return self.map

    def get_variable_value(self, variable_name):
        if variable_name in self.map[-1]:
            return self.map[-1][variable_name]['value']
        else:
            raise Undeclared('variable', variable_name)

    def find_function_def(self, identifier, arguments_num):
        for function_def in self.functions_def:
            if function_def.identifier == identifier and len(function_def.arguments) == arguments_num:
                return function_def

    def does_element_meet_conditions(self, element, conditions):
        operators = {
            '>': operator.gt,
            '<': operator.lt,
            '>=': operator.ge,
            '<=': operator.le,
            '==': operator.eq,
            '!=': operator.ne
        }
        for condition in conditions:
            operation, expression = condition.accept(self)
            operation = operators[operation]
            if not (operation(element, expression)):
                return False
        return True

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

    @staticmethod
    def is_value_type_correct(variable_value, variable_type):
        types_conversion = {
            'int': int,
            'float': float,
            'list': list,
            'string': str
        }
        return variable_type in types_conversion and types_conversion[variable_type] == type(variable_value)

    def save_variable(self, variable_name, variable_value):
        if variable_name in self.map[-1]:
            variable_type = self.map[-1][variable_name]['type']
            if self.is_value_type_correct(variable_value, variable_type):
                self.map[-1][variable_name]['value'] = variable_value
                return True
            raise InvalidValue(variable_type, type(variable_value).__name__)
        raise Undeclared('variable', variable_name)

    def try_variable_assign(self, operation, left_operand, right_operand):
        if operation == '==':
            if isinstance(left_operand, str):
                right_operand_value = right_operand
                if isinstance(right_operand, str):
                    right_operand_value = self.get_variable_value(right_operand)
                self.save_variable(left_operand, right_operand_value)
                return right_operand_value
            else:
                raise InvalidOperation('r-value', '=', 'r-value')

    # PRIMITIVES
    def visit_arithmetic_operator(self, node):
        pass

    def visit_comparison_operator(self, node):
        pass

    def visit_logical_operator(self, node):
        pass

    def visit_id(self, node):
        pass

    def visit_type(self, node):
        pass

    # SEMI-COMPLEX
    def visit_literal(self, node):
        pass

    def visit_unary_operation(self, node):
        pass

    def visit_list_element(self, node):
        pass

    def visit_variable_declaration(self, node):
        pass

    def visit_list_variable_declaration(self, node):
        pass

    def visit_list_comprehension_declaration(self, node):
        pass

    def visit_variable_assignment(self, node):
        pass

    def visit_list_variable_assignment(self, node):
        pass

    def visit_list_comprehension_assignment(self, node):
        pass

    def visit_function_argument(self, node):
        pass

    def visit_function_invocation(self, node):
        function_def = self.find_function_def(node.name, len(node.arguments))
        if function_def is not None:
            self.map.append({})

            arguments_value = []
            for argument in node.arguments:
                arguments_value.append(argument.accept(self))
            for argument in function_def.arguments:
                argument.accept(self)
            for i in range(0, len(arguments_value)):
                variable_name = function_def.arguments[i].identifier.accept(self)
                self.save_variable(variable_name, arguments_value[i])

            result = function_def.accept(self)
            self.map.pop()
            return result
        raise Undeclared('function', node.identifier.accept(self))

    def visit_single_condition(self, node):
        pass

    def visit_arithmetic_expression(self, node):
        left_operand = node.left_operand.accept(self)
        operation = node.operator
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
        pass

    # COMPLEX
    def visit_function_declaration(self, node):
        pass

    def visit_if_statement(self, node):
        pass

    def visit_while_statement(self, node):
        pass
