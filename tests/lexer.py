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
        """
        Generic method for lexer testing. Takes input and expected result as arguments.
        Produces every possible token from given input and compares collection's items one by one.

        :param string_input:
        :param expected_sequence_of_tokens:
        :return:
        """
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
        input_str = """foo"""
        expected_tokens = [TokenType.IDENTIFIER, "foo"]
        self.assert_expected_tokens(input_str, expected_tokens)

if __name__ == '__main__':
    unittest.main()


def init_lexer_for_test(test_string):
    source = Source(io.StringIO(test_string))
    return Lexer(source)