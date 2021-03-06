import copy

from src.parser.ast.semi_complex import *
from src.parser.ast.complex import *
from src.semantic_analyzer.symbol import *
from src.error_handling import *

INT_TYPE = Type(Token(TokenType.INT_KEYWORD))
FLOAT_TYPE = Type(Token(TokenType.FLOAT_KEYWORD))
STRING_TYPE = Type(Token(TokenType.STRING_KEYWORD))
LINT_TYPE = Type(Token(TokenType.INT_LIST_KEYWORD))
LFLOAT_TYPE = Type(Token(TokenType.FLOAT_LIST_KEYWORD))
LSTRING_TYPE = Type(Token(TokenType.STRING_LIST_KEYWORD))


class SemanticAnalyzer:
    def __init__(self):
        self.current_expected_type = None

    def start_analysis(self, program):
        return self.__analyze_scope(program, {}, {}, False, None)

    def __check_fun_declaration(self, fun_decl, var_symbols, fun_symbols):
        return_type = fun_decl.type
        fun_name = fun_decl.name.name
        args = fun_decl.arguments
        body = fun_decl.instructions

        arg_types = []
        for arg in args:
            arg_name = arg.name.name
            arg_type = arg.type
            new_var_symbol = VariableSymbol(arg_type, arg_name)
            var_symbols[arg_name] = new_var_symbol
            arg_types.append(arg_type)

        new_fun_symbol = FunctionSymbol(return_type, fun_name, arg_types)
        fun_symbols[fun_name] = new_fun_symbol
        self.__analyze_scope(body, var_symbols, fun_symbols, is_inside_fun=True, return_type=return_type)
        if not self.__check_if_return_in_fun_body(body, fun_name):
            SemanticNoReturnExpressionInFunBodyError(fun_name).fatal()

    def __check_if_return_in_fun_body(self, list_of_instruction, fun_name):
        for ins in list_of_instruction:
            if isinstance(ins, ReturnExpression):
                return True
            elif isinstance(ins, IfStatement):
                if self.__check_if_return_in_fun_body(ins.if_instructions, fun_name):
                    return True
                if self.__check_if_return_in_fun_body(ins.else_instructions, fun_name):
                    return True
            elif isinstance(ins, WhileStatement):
                if self.__check_if_return_in_fun_body(ins.instructions, fun_name):
                    return True
        return False

    def __check_var_declaration(self, var_decl, var_symbols, fun_symbols):
        var_name = var_decl.name.name
        if var_name in var_symbols:
            SemanticVariableRedeclarationError(var_name).fatal()
        self.current_expected_type = var_decl.type
        self.__check_r_value(var_decl.value, var_symbols, fun_symbols, var_decl.type)

        new_var_symbol = VariableSymbol(var_decl.type, var_name)
        var_symbols[var_name] = new_var_symbol

    def __check_list_var_declaration(self, list_var_decl, var_symbols, fun_symbols):
        list_var_name = list_var_decl.name.name
        if list_var_name in var_symbols:
            SemanticVariableRedeclarationError(list_var_name).fatal()
        list_var_type = list_var_decl.type

        if str(list_var_type) == str(LINT_TYPE):
            list_elem_type = INT_TYPE
        elif str(list_var_type) == str(LFLOAT_TYPE):
            list_elem_type = FLOAT_TYPE
        else:
            list_elem_type = STRING_TYPE

        self.current_expected_type = list_elem_type
        for value in list_var_decl.values:
            self.__check_r_value(value, var_symbols, fun_symbols, list_elem_type)

        new_var_symbol = VariableSymbol(list_var_decl.type, list_var_name)
        var_symbols[list_var_name] = new_var_symbol

    def __check_list_comprehension_declaration(self, list_cmprhnsn_decl, var_symbols, fun_symbols):
        list_var_name = list_cmprhnsn_decl.name.name
        if list_var_name in var_symbols:
            SemanticVariableRedeclarationError(list_var_name).fatal()
        list_var_type = list_cmprhnsn_decl.type
        if str(list_var_type) == str(LINT_TYPE):
            list_elem_type = INT_TYPE
        elif str(list_var_type) == str(LFLOAT_TYPE):
            list_elem_type = FLOAT_TYPE
        else:
            list_elem_type = STRING_TYPE

        self.current_expected_type = list_elem_type
        temp_for_id_symbol = VariableSymbol(list_elem_type, list_cmprhnsn_decl.for_id.name)
        temp_var_symbols = copy.deepcopy(var_symbols)
        temp_var_symbols[list_cmprhnsn_decl.for_id.name] = temp_for_id_symbol
        self.__check_r_value(list_cmprhnsn_decl.what_expression, temp_var_symbols, fun_symbols, list_elem_type)
        self.__check_r_value(list_cmprhnsn_decl.in_expression, var_symbols, fun_symbols, list_cmprhnsn_decl.type)

        new_var_symbol = VariableSymbol(list_cmprhnsn_decl.type, list_var_name)
        var_symbols[list_var_name] = new_var_symbol

    def __check_var_assignment(self, var_assignment, var_symbols, fun_symbols):
        var_name = var_assignment.name.name
        if var_name not in var_symbols:
            SemanticAssignmentWithoutDeclarationError(var_name).fatal()
        var_type = var_symbols[var_name].get_type()
        self.current_expected_type = var_type
        self.__check_r_value(var_assignment.value, var_symbols, fun_symbols, var_type)

    def __check_list_var_assignment(self, list_var_assignment, var_symbols, fun_symbols):
        list_var_name = list_var_assignment.name.name
        if list_var_name not in var_symbols:
            SemanticAssignmentWithoutDeclarationError(list_var_name).fatal()
        list_var_type = var_symbols[list_var_name].get_type()

        if str(list_var_type) == str(LINT_TYPE):
            list_elem_type = INT_TYPE
        elif str(list_var_type) == str(LFLOAT_TYPE):
            list_elem_type = FLOAT_TYPE
        else:
            list_elem_type = STRING_TYPE

        self.current_expected_type = list_elem_type
        for value in list_var_assignment.values:
            self.__check_r_value(value, var_symbols, fun_symbols, list_elem_type)

    def __check_list_comprehension_assignment(self, list_cmprhnsn_assignment, var_symbols, fun_symbols):
        list_var_name = list_cmprhnsn_assignment.name.name
        if list_var_name not in var_symbols:
            SemanticAssignmentWithoutDeclarationError(list_var_name).fatal()
        list_var_type = var_symbols[list_var_name].get_type()

        if str(list_var_type) == str(LINT_TYPE):
            list_elem_type = INT_TYPE
        elif str(list_var_type) == str(LFLOAT_TYPE):
            list_elem_type = FLOAT_TYPE
        else:
            list_elem_type = STRING_TYPE

        self.current_expected_type = list_elem_type
        temp_for_id_symbol = VariableSymbol(list_elem_type, list_cmprhnsn_assignment.for_id.name)
        temp_var_symbols = copy.deepcopy(var_symbols)
        temp_var_symbols[list_cmprhnsn_assignment.for_id.name] = temp_for_id_symbol
        self.__check_r_value(list_cmprhnsn_assignment.what_expression, temp_var_symbols, fun_symbols, list_elem_type)

        self.__check_r_value(list_cmprhnsn_assignment.in_expression, var_symbols, fun_symbols,
                             list_var_type)

    def __check_if_stmt(self, if_stmt, var_symbols, fun_symbols, is_inside_fun, return_type):
        condition = if_stmt.condition
        self.__check_condition(condition, var_symbols, fun_symbols)
        if_instructions = if_stmt.if_instructions
        else_instructions = if_stmt.else_instructions
        self.__analyze_scope(if_instructions, var_symbols.copy(), fun_symbols.copy(), is_inside_fun, return_type)
        self.__analyze_scope(else_instructions, var_symbols.copy(), fun_symbols.copy(), is_inside_fun, return_type)

    def __check_while_stmt(self, while_stmt, var_symbols, fun_symbols, is_inside_fun, return_type):
        condition = while_stmt.condition
        self.__check_condition(condition, var_symbols, fun_symbols)
        instructions = while_stmt.instructions
        self.__analyze_scope(instructions, var_symbols.copy(), fun_symbols.copy(), is_inside_fun, return_type)

    def __check_return_expr(self, return_expr, var_symbols, fun_symbols, is_inside_fun, return_type):
        if not is_inside_fun:
            SemanticReturnNotInsideFunctionBodyError().fatal()
        self.current_expected_type = return_type
        self.__check_r_value(return_expr.value, var_symbols, fun_symbols, return_type)

    def __check_arithmetic_expr(self, arithmetic_expr, var_symbols, fun_symbols):
        left = arithmetic_expr.left_operand
        right = arithmetic_expr.right_operand
        self.__check_r_value(left, var_symbols, fun_symbols, self.current_expected_type)
        self.__check_r_value(right, var_symbols, fun_symbols, self.current_expected_type)

    def __check_fun_invocation(self, fun_invocation, var_symbols, fun_symbols):
        fun_name = fun_invocation.name.name
        if fun_name not in fun_symbols:
            SemanticNoSuchFunctionError(fun_name).fatal()

        args = fun_invocation.arguments
        expected_types = fun_symbols[fun_name].arg_types

        if len(args) != len(expected_types):
            SemanticInvalidNumberOfArgsError(len(args), len(expected_types)).fatal()

        invoke_arg_types = []
        for arg in args:
            invoke_arg_types.append(self.__get_fun_invocation_argument_type(arg, var_symbols))

        for i in range(len(args)):
            if str(invoke_arg_types[i]) != str(expected_types[i]):
                SemanticTypesOfArgsInFunInvocationError(fun_name, expected_types, invoke_arg_types).fatal()

    @staticmethod
    def __get_fun_invocation_argument_type(arg, var_symbols):
        if isinstance(arg, Literal):
            return arg.type
        elif isinstance(arg, Id):
            return var_symbols[arg.name].get_type()
        elif isinstance(arg, ArithmeticExpression):
            return INT_TYPE

    def __check_condition(self, condition, var_symbols, fun_symbols):
        if isinstance(condition, Literal):
            self.__check_literal(condition, expected_type=None)
        elif isinstance(condition, Id):
            self.__check_var_id(condition, var_symbols, expected_type=None)
        elif isinstance(condition, SingleCondition):
            self.__check_comparison(condition, var_symbols)

    def __check_comparison(self, comparison, var_symbols):
        self.__check_r_value(comparison.left, var_symbols, fun_symbols=None, expected_type=None)
        self.__check_r_value(comparison.right, var_symbols, fun_symbols=None, expected_type=None)

    def __check_r_value(self, r_value, var_symbols, fun_symbols, expected_type):
        if isinstance(r_value, Literal):
            self.__check_literal(r_value, expected_type)
        elif isinstance(r_value, Id):
            self.__check_var_id(r_value, var_symbols, expected_type)
        elif isinstance(r_value, ArithmeticExpression):
            self.__check_arithmetic_expr(r_value, var_symbols, fun_symbols)

    @staticmethod
    def __get_type_of_r_value(r_value, var_symbols):
        if isinstance(r_value, Literal):
            return r_value.type
        elif isinstance(r_value, Id):
            return var_symbols[r_value.name].get_type()
        elif isinstance(r_value, ArithmeticExpression):
            return INT_TYPE

    @staticmethod
    def __check_var_id(var_id, var_symbols, expected_type):
        var_name = var_id.name
        if var_name not in var_symbols:
            SemanticUnknownSymbolError(var_name).fatal()
        if expected_type is not None and str(expected_type) != str(var_symbols[var_name].type):
            SemanticInvalidTypeError(expected_type, var_symbols[var_name].type).fatal()

    @staticmethod
    def __check_literal(literal, expected_type):
        if expected_type is not None and str(literal.type) != str(expected_type):
            SemanticInvalidTypeError(expected_type, literal.type).fatal()

    def __analyze_scope(self, list_of_instructions, var_symbols, fun_symbols, is_inside_fun, return_type):
        for ins in list_of_instructions:
            if isinstance(ins, FunctionDeclaration):
                self.__check_fun_declaration(ins, var_symbols.copy(), fun_symbols)

            elif isinstance(ins, VariableDeclaration):
                self.__check_var_declaration(ins, var_symbols, fun_symbols)

            elif isinstance(ins, ListVariableDeclaration):
                self.__check_list_var_declaration(ins, var_symbols, fun_symbols)

            elif isinstance(ins, ListComprehensionDeclaration):
                self.__check_list_comprehension_declaration(ins, var_symbols, fun_symbols)

            elif isinstance(ins, VariableAssignment):
                self.__check_var_assignment(ins, var_symbols, fun_symbols)

            elif isinstance(ins, ListVariableAssignment):
                self.__check_list_var_assignment(ins, var_symbols, fun_symbols)

            elif isinstance(ins, ListComprehensionAssignment):
                self.__check_list_comprehension_assignment(ins, var_symbols, fun_symbols)

            elif isinstance(ins, IfStatement):
                self.__check_if_stmt(ins, var_symbols.copy(), fun_symbols.copy(), is_inside_fun, return_type)

            elif isinstance(ins, WhileStatement):
                self.__check_while_stmt(ins, var_symbols.copy(), fun_symbols.copy(), is_inside_fun, return_type)

            elif isinstance(ins, FunctionInvocation):
                self.__check_fun_invocation(ins, var_symbols, fun_symbols)

            elif isinstance(ins, ReturnExpression):
                self.__check_return_expr(ins, var_symbols, fun_symbols, is_inside_fun, return_type)

        return list_of_instructions
