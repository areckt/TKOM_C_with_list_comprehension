import io
import unittest

from src.lexer.source import Source
from src.lexer.lexer import Lexer
from src.lexer.token import TokenType, Token


class LexerTest(unittest.TestCase):
    def test_eof(self):
        lexer = init_lexer_for_test("")
        token = lexer.build_and_get_token()
        self.assertEqual(token.get_type(), TokenType.EOF_SYMBOL)

    def assert_expected_tokens(self, string_input, expected_sequence_of_tokens):
        # Method for lexer testing. Takes input and expected result as arguments.
        # Produces every possible token from given input and compares collection's items one by one.

        lexer = init_lexer_for_test(string_input)
        tokens = []
        token = lexer.build_and_get_token()
        while token.type != TokenType.EOF_SYMBOL:
            tokens.append(token)
            token = lexer.build_and_get_token()

        for i in range(len(expected_sequence_of_tokens)):
            self.assertEqual(tokens[i].get_type(), expected_sequence_of_tokens[i].get_type())
            self.assertEqual(tokens[i].get_value(), expected_sequence_of_tokens[i].get_value())

    # #################
    # vvv T E S T S vvv
    # #################

    def test_one_identifier(self):
        input_str = "foo"
        expected_tokens = [Token(TokenType.IDENTIFIER, "foo")]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_many_identifiers(self):
        input_str = "foo bar baz"
        expected_tokens = [
            Token(TokenType.IDENTIFIER, "foo"),
            Token(TokenType.IDENTIFIER, "bar"),
            Token(TokenType.IDENTIFIER, "baz")
        ]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_return_keyword(self):
        input_str = "return"
        expected_tokens = [Token(TokenType.RETURN_KEYWORD)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_while_keyword(self):
        input_str = "while"
        expected_tokens = [Token(TokenType.WHILE_KEYWORD)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_if_keyword(self):
        input_str = "if"
        expected_tokens = [Token(TokenType.IF_KEYWORD)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_else_keyword(self):
        input_str = "else"
        expected_tokens = [Token(TokenType.ELSE_KEYWORD)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_for_keyword(self):
        input_str = "for"
        expected_tokens = [Token(TokenType.FOR_KEYWORD)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_in_keyword(self):
        input_str = "in"
        expected_tokens = [Token(TokenType.IN_KEYWORD)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_int_keyword(self):
        input_str = "int"
        expected_tokens = [Token(TokenType.INT_KEYWORD)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_int_list_keyword(self):
        input_str = "int[]"
        expected_tokens = [Token(TokenType.INT_LIST_KEYWORD)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_float_keyword(self):
        input_str = "float"
        expected_tokens = [Token(TokenType.FLOAT_KEYWORD)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_float_list_keyword(self):
        input_str = "float[]"
        expected_tokens = [Token(TokenType.FLOAT_LIST_KEYWORD)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_string_keyword(self):
        input_str = "string"
        expected_tokens = [Token(TokenType.STRING_KEYWORD)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_string_list_keyword(self):
        input_str = "string[]"
        expected_tokens = [Token(TokenType.STRING_LIST_KEYWORD)]
        self.assert_expected_tokens(input_str, expected_tokens)


if __name__ == '__main__':
    unittest.main()


def init_lexer_for_test(test_string):
    source = Source(io.StringIO(test_string))
    return Lexer(source)
