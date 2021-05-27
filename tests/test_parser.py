import io
import unittest

from src.lexer.source import Source
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.parser.ast.semi_complex import *
from src.parser.ast.complex import *


class ParserTest(unittest.TestCase):
    def assert_instructions(self, list_of_instructions, list_of_expected):
        for i in range(0, len(list_of_expected)):
            current_instruction = list_of_instructions[i]
            current_expected = list_of_expected[i]
            self.assertTrue(isinstance(current_instruction, current_expected))

    # INT DECLARATION
    def test_int_variable_declaration(self):
        input_str = """int i = 5;"""
        list_of_expected = [VariableDeclaration]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_type_in_int_variable_declaration(self):
        input_str = """int i = 5;"""
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        var_type = program[0].type.type
        self.assertTrue(var_type == Types.INT)

    def test_value_in_int_variable_declaration(self):
        input_str = """int i = 5;"""
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        value = program[0].value.get_value()
        self.assertEqual(value, 5)

    # FLOAT DECLARATION
    def test_float_variable_declaration(self):
        input_str = """float temp = 36.5;"""
        list_of_expected = [VariableDeclaration]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_type_in_float_variable_declaration(self):
        input_str = """float temp = 36.5;"""
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        var_type = program[0].type.type
        self.assertTrue(var_type == Types.FLOAT)

    def test_value_in_float_variable_declaration(self):
        input_str = """float temp = 36.5;"""
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        value = program[0].value.get_value()
        self.assertEqual(value, 36.5)

    # STRING DECLARATION
    def test_string_variable_declaration(self):
        input_str = """string word = "great!";"""
        list_of_expected = [VariableDeclaration]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_type_in_string_variable_declaration(self):
        input_str = """string word = "great!";"""
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        var_type = program[0].type.type
        self.assertTrue(var_type == Types.STRING)

    def test_value_in_string_variable_declaration(self):
        input_str = """string word = "great!";"""
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        value = program[0].value.get_value()
        self.assertEqual(value, "great!")

    # DECLARATION OF VARIABLE WITH FORBIDDEN ID
    def test_variable_declaration_with_forbidden_id_1(self):
        input_str = """int for = 5;"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    def test_variable_declaration_with_forbidden_id_2(self):
        input_str = """float while = 36.7;"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    def test_variable_declaration_with_forbidden_id_3(self):
        input_str = """string else = "great!";"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    def test_variable_declaration_with_forbidden_id_4(self):
        input_str = """int int = 5;"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    def test_variable_declaration_with_forbidden_id_5(self):
        input_str = """float float = 36.7;"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    def test_variable_declaration_with_forbidden_id_6(self):
        input_str = """string string = "great!";"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    # DECLARATION WITH NO INITIALIZATION
    def test_int_variable_declaration_without_initialization(self):
        input_str = """int i;"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    def test_float_variable_declaration_without_initialization(self):
        input_str = """float temp;"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    def test_string_variable_declaration_without_initialization(self):
        input_str = """string s;"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    def test_lint_variable_declaration_without_initialization(self):
        input_str = """lint nums;"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    def test_lfloat_variable_declaration_without_initialization(self):
        input_str = """lfloat temps;"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    def test_lstring_variable_declaration_without_initialization(self):
        input_str = """lstring chars;"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    # LINT DECLARATION
    def test_lint_list_declaration(self):
        input_str = """lint i = [1, 2, 3];"""
        list_of_expected = [ListVariableDeclaration]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_type_in_lint_list_declaration(self):
        input_str = """lint i = [1, 2, 3];"""
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        var_type = program[0].type.type
        self.assertEqual(var_type, ListTypes.LINT)

    def test_values_in_lint_list_declaration(self):
        input_str = """lint i = [1, 2, 3];"""
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        values = [literal.get_value() for literal in program[0].values]
        self.assertEqual(values, [1, 2, 3])

    # LFLOAT DECLARATION
    def test_lfloat_list_declaration(self):
        input_str = """lfloat temps = [36.7, 36.2, 37.1];"""
        list_of_expected = [ListVariableDeclaration]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_type_in_lfloat_list_declaration(self):
        input_str = """lfloat temps = [36.7, 36.2, 37.1];"""
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        var_type = program[0].type.type
        self.assertEqual(var_type, ListTypes.LFLOAT)

    def test_values_in_lfloat_list_declaration(self):
        input_str = """lfloat temps = [36.7, 36.2, 37.1];"""
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        values = [literal.get_value() for literal in program[0].values]
        self.assertEqual(values, [36.7, 36.2, 37.1])

    # LSTRING DECLARATION
    def test_lstring_list_declaration(self):
        input_str = """lstring chars = ["a", "b", "c"];"""
        list_of_expected = [ListVariableDeclaration]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_type_in_lstring_list_declaration(self):
        input_str = """lstring chars = ["a", "b", "c"];"""
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        var_type = program[0].type.type
        self.assertEqual(var_type, ListTypes.LSTRING)

    def test_values_in_lstring_list_declaration(self):
        input_str = """lstring chars = ["a", "b", "c"];"""
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        values = [literal.get_value() for literal in program[0].values]
        self.assertEqual(values, ["a", "b", "c"])

    # STANDARD TYPE ASSIGNMENT
    def test_int_variable_assignment(self):
        input_str = """i = 5;"""
        list_of_expected = [VariableAssignment]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_float_variable_assignment(self):
        input_str = """temp = 36.7;"""
        list_of_expected = [VariableAssignment]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_string_variable_assignment(self):
        input_str = """char = "a";"""
        list_of_expected = [VariableAssignment]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    # LIST TYPE ASSIGNMENT
    def test_lint_variable_assignment(self):
        input_str = """nums = [1, 2, 3];"""
        list_of_expected = [ListVariableAssignment]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_lfloat_variable_assignment(self):
        input_str = """nums = [1.1, 2.2, 3.3];"""
        list_of_expected = [ListVariableAssignment]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_lstring_variable_assignment(self):
        input_str = """chars = ["a", "b", "c"];"""
        list_of_expected = [ListVariableAssignment]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    # ARITHMETIC EXPRESSIONS
    def test_arithmetic_expression_no_multiplication_no_brackets(self):
        input_str = """i = a+b+c;"""
        list_of_expected = [VariableAssignment]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_arithmetic_expression_multiplication_no_brackets(self):
        input_str = """i = a+b*c;"""
        list_of_expected = [VariableAssignment]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_arithmetic_expression_multiplication_brackets(self):
        input_str = """i = a*(b+(c*d));"""
        list_of_expected = [VariableAssignment]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    # FUNCTION DECLARATION
    def test_function_declaration_no_args_no_body(self):
        input_str = """int fun(){}"""
        list_of_expected = [FunctionDeclaration]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_function_declaration_args_no_body(self):
        input_str = """int fun(float t, string s){}"""
        list_of_expected = [FunctionDeclaration]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_function_declaration_args_body(self):
        input_str = """int fun(float t, string s){return 0;}"""
        list_of_expected = [FunctionDeclaration]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    # FUNCTION INVOCATION
    def test_function_invocation_no_args(self):
        input_str = """fun();"""
        list_of_expected = [FunctionInvocation]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_function_invocation_args(self):
        input_str = """fun(10, temp, "Hey", 0.4);"""
        list_of_expected = [FunctionInvocation]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    # RETURN
    def test_return_no_value(self):
        input_str = """return;"""
        list_of_expected = [ReturnExpression]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_return_value(self):
        input_str = """return i;"""
        list_of_expected = [ReturnExpression]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    # WHILE
    def test_while_no_body(self):
        input_str = """while(i < 10){}"""
        list_of_expected = [WhileStatement]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_while_body(self):
        input_str = """while(i < 10){i = i + 1;}"""
        list_of_expected = [WhileStatement]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    # IF & ELSE
    def test_if_no_body_no_else(self):
        input_str = """if(i > 10){}"""
        list_of_expected = [IfStatement]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_if_body_no_else(self):
        input_str = """if(i > 10){i = i - 1;}"""
        list_of_expected = [IfStatement]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_if_body_else(self):
        input_str = """if(i > 10){i = i - 1;}else{i = i * 2;}"""
        list_of_expected = [IfStatement]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    # LIST COMPREHENSION
    def test_list_comprehension_declaration(self):
        input_str = """lint squares = [n*n for n in nums];"""
        list_of_expected = [ListComprehensionDeclaration]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_list_comprehension_assignment(self):
        input_str = """squares = [n*n for n in nums];"""
        list_of_expected = [ListComprehensionAssignment]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_bad_list_declaration_with_list_comprehension_in_the_middle(self):
        input_str = """lint squares = [1, 4, n*n for n in nums, 25];"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    # LIST ELEMENTS
    def test_assign_list_element_literal_index(self):
        input_str = """temp = nums[2];"""
        list_of_expected = [VariableAssignment]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_assign_list_element_id_index(self):
        input_str = """temp = nums[i];"""
        list_of_expected = [VariableAssignment]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_assign_list_element_arithmetic_expression_index(self):
        input_str = """temp = nums[a*(2+b)/c];"""
        list_of_expected = [VariableAssignment]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    # UNARY OPERATORS - '-' as minus, '_' as length_op and '!' as reverse_op
    def test_minus_as_unary_operator_in_declaration(self):
        input_str = """float y = -x;"""
        list_of_expected = [VariableDeclaration]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_minus_as_unary_operator_in_assignment(self):
        input_str = """y = -x;"""
        list_of_expected = [VariableAssignment]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_length_operator_in_declaration(self):
        input_str = """int length = _nums;"""
        list_of_expected = [VariableDeclaration]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_length_operator_in_assignment(self):
        input_str = """length = _nums;"""
        list_of_expected = [VariableAssignment]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    def test_reverse_operator_in_assignment(self):
        input_str = """temp = !nums;"""
        list_of_expected = [VariableAssignment]
        parser = init_parser_for_test(input_str)
        program = parser.parse_program()
        self.assert_instructions(program, list_of_expected)

    # COMMON MISTAKES
    def test_missing_close_quotation_mark(self):
        input_str = """string word = "error;"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    def test_missing_semicolon(self):
        input_str = """lint nums = [1, 2, 3]"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    def test_missing_bracket(self):
        input_str = """float result = 2*(1+b / (c+2);"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    def test_missing_close_list_bracket(self):
        input_str = """lint nums = [1, 2, 3;"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    def test_missing_close_block_bracket(self):
        input_str = """while (i < 10){"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    def test_missing_open_bracket(self):
        input_str = """while i < 10){}"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    def test_assign_literal_to_list_type(self):
        input_str = """lint nums = 2;"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    def test_assign_list_to_standard_type(self):
        input_str = """int nums = [1, 2, 3];"""
        parser = init_parser_for_test(input_str)
        with self.assertRaises(Exception):
            parser.parse_program()

    # LONGER EXAMPLES
    def test_nested_instructions(self):
        input_str = """
        int fun(int a, int b, int c){
            return a+b+c;
        }

        int i = 1;
        while(i < 15){
            if(i<10){
                i = i+10;
                string str = "example";
            }
            else{
                fun(1,2,3);
            }
        }
        return 1;
        """
        parser = init_parser_for_test(input_str)

        first_level = parser.parse_program()
        first_level_expected = [FunctionDeclaration, VariableDeclaration, WhileStatement,
                                ReturnExpression]

        fun_decl = first_level[0].instructions
        fun_decl_expected = [ReturnExpression]

        while_stmt = first_level[2].instructions
        while_stmt_expected = [IfStatement]

        nested_if_stmt = while_stmt[0].if_instructions
        nested_if_stmt_expected = [VariableAssignment, VariableDeclaration]
        nested_else_stmt = while_stmt[0].else_instructions
        nested_else_stmt_expected = [FunctionInvocation]

        self.assert_instructions(first_level, first_level_expected)
        self.assert_instructions(fun_decl, fun_decl_expected)
        self.assert_instructions(while_stmt, while_stmt_expected)
        self.assert_instructions(nested_if_stmt, nested_if_stmt_expected)
        self.assert_instructions(nested_else_stmt, nested_else_stmt_expected)


if __name__ == '__main__':
    unittest.main()


def init_parser_for_test(test_string):
    source = Source(io.StringIO(test_string))
    lexer = Lexer(source)
    return Parser(lexer)
