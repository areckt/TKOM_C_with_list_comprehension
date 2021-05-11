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


if __name__ == '__main__':
    unittest.main()


def init_parser_for_test(test_string):
    source = Source(io.StringIO(test_string))
    lexer = Lexer(source)
    return Parser(lexer)
