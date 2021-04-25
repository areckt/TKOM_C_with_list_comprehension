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
            a, b = tokens[i].get_type(), expected_sequence_of_tokens[i].get_type()
            c, d = tokens[i].get_value(), expected_sequence_of_tokens[i].get_value()
            # self.assertEqual(tokens[i].get_type(), expected_sequence_of_tokens[i].get_type())
            # self.assertEqual(tokens[i].get_value(), expected_sequence_of_tokens[i].get_value())
            self.assertEqual(b, a)
            self.assertEqual(d, c)

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

    def test_identifiers_similar_to_keywords(self):
        input_str = "ford wwhile if2"
        expected_tokens = [
            Token(TokenType.IDENTIFIER, "ford"),
            Token(TokenType.IDENTIFIER, "wwhile"),
            Token(TokenType.IDENTIFIER, "if2")
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

    def test_semicolon(self):
        input_str = ";"
        expected_tokens = [Token(TokenType.SEMICOLON)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_comma(self):
        input_str = ","
        expected_tokens = [Token(TokenType.COMMA)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_open_bracket(self):
        input_str = "("
        expected_tokens = [Token(TokenType.OPEN_BRACKET)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_close_bracket(self):
        input_str = ")"
        expected_tokens = [Token(TokenType.CLOSE_BRACKET)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_open_block(self):
        input_str = "{"
        expected_tokens = [Token(TokenType.OPEN_BLOCK)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_close_block(self):
        input_str = "}"
        expected_tokens = [Token(TokenType.CLOSE_BLOCK)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_open_list(self):
        input_str = "["
        expected_tokens = [Token(TokenType.OPEN_LIST)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_close_list(self):
        input_str = "]"
        expected_tokens = [Token(TokenType.CLOSE_LIST)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_plus(self):
        input_str = "+"
        expected_tokens = [Token(TokenType.PLUS)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_minus(self):
        input_str = "-"
        expected_tokens = [Token(TokenType.MINUS)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_multiply(self):
        input_str = "*"
        expected_tokens = [Token(TokenType.MULTIPLY)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_divide(self):
        input_str = "/"
        expected_tokens = [Token(TokenType.DIVIDE)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_modulo(self):
        input_str = "%"
        expected_tokens = [Token(TokenType.MODULO)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_length_op(self):
        input_str = "_"
        expected_tokens = [Token(TokenType.LENGTH_OP)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_and(self):
        input_str = "&&"
        expected_tokens = [Token(TokenType.AND)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_or(self):
        input_str = "||"
        expected_tokens = [Token(TokenType.OR)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_not(self):
        input_str = "!"
        expected_tokens = [Token(TokenType.NOT)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_less(self):
        input_str = "<"
        expected_tokens = [Token(TokenType.LESS)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_less_or_equal(self):
        input_str = "<="
        expected_tokens = [Token(TokenType.LESS_OR_EQUAL)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_equal(self):
        input_str = "=="
        expected_tokens = [Token(TokenType.EQUAL)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_not_equal(self):
        input_str = "!="
        expected_tokens = [Token(TokenType.NOT_EQUAL)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_greater(self):
        input_str = ">"
        expected_tokens = [Token(TokenType.GREATER)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_greater_or_equal(self):
        input_str = ">="
        expected_tokens = [Token(TokenType.GREATER_OR_EQUAL)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_assign(self):
        input_str = "="
        expected_tokens = [Token(TokenType.ASSIGN)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_int_literal(self):
        input_str = "546"
        expected_tokens = [Token(TokenType.INT_LITERAL, 546)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_int_literal_zero(self):
        input_str = "0"
        expected_tokens = [Token(TokenType.INT_LITERAL, 0)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_float_literal(self):
        input_str = "36.7"
        expected_tokens = [Token(TokenType.FLOAT_LITERAL, 36.7)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_float_literal_with_two_points_starting_with_zero(self):
        input_str = "0.5.5a5..5...f5"
        expected_tokens = [Token(TokenType.UNKNOWN, "0.5.5a5..5...f5")]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_float_literal_with_two_points_starting_with_nonzero(self):
        input_str = "5.5.5a5..5...f5"
        expected_tokens = [Token(TokenType.UNKNOWN, "5.5.5a5..5...f5")]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_float_literal_smaller_than_one(self):
        input_str = "0.12345"
        expected_tokens = [Token(TokenType.FLOAT_LITERAL, 0.12345)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_string_literal(self):
        input_str = '"example string 123 !@#"'
        expected_tokens = [Token(TokenType.STRING_LITERAL, "example string 123 !@#")]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_string_literal_with_escape_characters(self):
        input_str = '''"example\\n \\\"string\\t123 !@#"'''
        expected_tokens = [Token(TokenType.STRING_LITERAL, '''example\\n \\\"string\\t123 !@#''')]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_string_literal_ending_with_escape_character(self):
        input_str = '''"very bad string\\"'''
        expected_tokens = [Token(TokenType.UNKNOWN)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_string_literal_with_no_closing_quotation_mark(self):
        input_str = '"Oh no, I forgot about closing quotation mark!'
        expected_tokens = [Token(TokenType.UNKNOWN)]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_unknown(self):
        input_str = "list["
        expected_tokens = [Token(TokenType.UNKNOWN, "list[")]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_longer_code_1(self):
        input_str = """ string foo(string name){
                            string greeting = "Hello, " + name;
                            return greeting;
                        }"""
        expected_tokens = [
            Token(TokenType.STRING_KEYWORD),
            Token(TokenType.IDENTIFIER, "foo"),
            Token(TokenType.OPEN_BRACKET),
            Token(TokenType.STRING_KEYWORD),
            Token(TokenType.IDENTIFIER, "name"),
            Token(TokenType.CLOSE_BRACKET),
            Token(TokenType.OPEN_BLOCK),
            Token(TokenType.STRING_KEYWORD),
            Token(TokenType.IDENTIFIER, "greeting"),
            Token(TokenType.ASSIGN),
            Token(TokenType.STRING_LITERAL, "Hello, "),
            Token(TokenType.PLUS),
            Token(TokenType.IDENTIFIER, "name"),
            Token(TokenType.SEMICOLON),
            Token(TokenType.RETURN_KEYWORD),
            Token(TokenType.IDENTIFIER, "greeting"),
            Token(TokenType.SEMICOLON),
            Token(TokenType.CLOSE_BLOCK)
        ]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_longer_code_2(self):
        input_str = """ int foo(){
                            int num = 5;
                            string s = "";
                            while (num > 0){
                                s = s + "a";
                                num = num - 1;
                            }
                            return _s;
                        }"""
        expected_tokens = [
            Token(TokenType.INT_KEYWORD),
            Token(TokenType.IDENTIFIER, "foo"),
            Token(TokenType.OPEN_BRACKET),
            Token(TokenType.CLOSE_BRACKET),
            Token(TokenType.OPEN_BLOCK),
            Token(TokenType.INT_KEYWORD),
            Token(TokenType.IDENTIFIER, "num"),
            Token(TokenType.ASSIGN),
            Token(TokenType.INT_LITERAL, 5),
            Token(TokenType.SEMICOLON),
            Token(TokenType.STRING_KEYWORD),
            Token(TokenType.IDENTIFIER, "s"),
            Token(TokenType.ASSIGN),
            Token(TokenType.STRING_LITERAL, ""),
            Token(TokenType.SEMICOLON),
            Token(TokenType.WHILE_KEYWORD),
            Token(TokenType.OPEN_BRACKET),
            Token(TokenType.IDENTIFIER, "num"),
            Token(TokenType.GREATER),
            Token(TokenType.INT_LITERAL, 0),
            Token(TokenType.CLOSE_BRACKET),
            Token(TokenType.OPEN_BLOCK),
            Token(TokenType.IDENTIFIER, "s"),
            Token(TokenType.ASSIGN),
            Token(TokenType.IDENTIFIER, "s"),
            Token(TokenType.PLUS),
            Token(TokenType.STRING_LITERAL, "a"),
            Token(TokenType.SEMICOLON),
            Token(TokenType.IDENTIFIER, "num"),
            Token(TokenType.ASSIGN),
            Token(TokenType.IDENTIFIER, "num"),
            Token(TokenType.MINUS),
            Token(TokenType.INT_LITERAL, 1),
            Token(TokenType.SEMICOLON),
            Token(TokenType.CLOSE_BLOCK),
            Token(TokenType.RETURN_KEYWORD),
            Token(TokenType.LENGTH_OP),
            Token(TokenType.IDENTIFIER, "s"),
            Token(TokenType.SEMICOLON),
            Token(TokenType.CLOSE_BLOCK),
        ]
        self.assert_expected_tokens(input_str, expected_tokens)

    def test_longer_code_3(self):
        input_str = """ int[] squareList(int[] nums) {
                            int[] result = [n*n for n in nums];
                            return !result;
                        }"""
        expected_tokens = [
            Token(TokenType.INT_LIST_KEYWORD),
            Token(TokenType.IDENTIFIER, "squareList"),
            Token(TokenType.OPEN_BRACKET),
            Token(TokenType.INT_LIST_KEYWORD),
            Token(TokenType.IDENTIFIER, "nums"),
            Token(TokenType.CLOSE_BRACKET),
            Token(TokenType.OPEN_BLOCK),
            Token(TokenType.INT_LIST_KEYWORD),
            Token(TokenType.IDENTIFIER, "result"),
            Token(TokenType.ASSIGN),
            Token(TokenType.OPEN_LIST),
            Token(TokenType.IDENTIFIER, "n"),
            Token(TokenType.MULTIPLY),
            Token(TokenType.IDENTIFIER, "n"),
            Token(TokenType.FOR_KEYWORD),
            Token(TokenType.IDENTIFIER, "n"),
            Token(TokenType.IN_KEYWORD),
            Token(TokenType.IDENTIFIER, "nums"),
            Token(TokenType.CLOSE_LIST),
            Token(TokenType.SEMICOLON),
            Token(TokenType.RETURN_KEYWORD),
            Token(TokenType.NOT),
            Token(TokenType.IDENTIFIER, "result"),
            Token(TokenType.SEMICOLON),
            Token(TokenType.CLOSE_BLOCK),
        ]
        self.assert_expected_tokens(input_str, expected_tokens)


if __name__ == '__main__':
    unittest.main()


def init_lexer_for_test(test_string):
    source = Source(io.StringIO(test_string))
    return Lexer(source)
