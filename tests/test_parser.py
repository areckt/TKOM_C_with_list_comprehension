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
        var_type = program[0].type
        self.assertTrue(isinstance(var_type, Type))

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
        var_type = program[0].type
        self.assertTrue(isinstance(var_type, Type))

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
        var_type = program[0].type
        self.assertTrue(isinstance(var_type, Type))



if __name__ == '__main__':
    unittest.main()


def init_parser_for_test(test_string):
    source = Source(io.StringIO(test_string))
    lexer = Lexer(source)
    return Parser(lexer)
