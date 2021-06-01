class SemanticAnalyzer:
    def __init__(self):
        pass

    def start_analysis(self, program):
        return self.__analyze_scope(program, {}, {}, False, None)

    def __check_fun_declaration(self, fun_decl, var_symbols, fun_symbols):
        pass

    def __check_if_return_in_fun_body(self, list_of_instruction, fun_name):
        pass

    def __check_var_declaration(self, var_decl, var_symbols, fun_symbols):
        pass

    def __check_var_assignment(self, var_assignment, var_symbols, fun_symbols):
        pass

    def __check_if_stmt(self, if_stmt, var_symbols, fun_symbols, is_inside_fun, return_type):
        pass

    def __check_while_stmt(self, while_stmt, var_symbols, fun_symbols, is_inside_fun, return_type):
        pass

    def __check_return_expr(self, return_expr, var_symbols, fun_symbols, is_inside_fun, return_type):
        pass

    def __check_arithmetic_expr(self, arithmetic_expr, var_symbols, fun_symbols):
        pass

    def __check_fun_invocation(self, fun_invocation, var_symbols, fun_symbols):
        pass

    def __get_fun_invocation_argument_type(self, arg, var_symbols):
        pass

    def __check_condition(self, condition, var_symbols, fun_symbols):
        pass

    def __check_comparison(self, comparison, var_symbols):
        pass

    def __check_r_value(self, r_value, var_symbols, fun_symbols, expected_type):
        pass

    def __get_type_of_r_value(self, r_value, var_symbols):
        pass

    def __check_var_id(self, var_id, var_symbols, expected_type):
        pass

    def __check_literal(self, literal, expected_type):
        pass

    def __analyze_scope(self, list_of_instructions, var_symbols, fun_symbols, is_inside_fun, return_type):
        pass
