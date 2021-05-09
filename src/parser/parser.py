from src.error_handling import ParserError, ParserSyntaxError
from src.lexer.token import TokenType
from src.parser.ast.complex import *
from src.parser.ast.semi_complex import *
from src.parser.ast.primitives import *
from src.parser.parser_utils import ParserUtils


class Parser:
    def __init__(self, lexer):
        self.__lexer = lexer
        self.__current_token = None
        self.__get_next_token()

    def parse_program(self):
        program = []
        while self.__get_current_token().get_type() != TokenType.EOF_SYMBOL:
            new_ins = self.__parse_instruction()
            print(new_ins)
            program.append(new_ins)
        return program

    def __parse_instruction(self):
        possible_instruction = self.__parse_declaration() or \
                               self.__parse_id_starting() or \
                               self.__parse_return() or \
                               self.__parse_while() or \
                               self.__parse_if()

        if not possible_instruction:
            ParserError(self.__get_position(), "UNKNOWN INSTRUCTION").warning()
        return possible_instruction

    def __parse_declaration(self):
        possible_type_token = self.__check_if_one_of_tokens(ParserUtils.type_tokens)
        if not possible_type_token:
            return None

        id_token = self.__consume_token(TokenType.IDENTIFIER)

        possible_function_declaration = self.__parse_function_declaration(possible_type_token, id_token)
        if possible_function_declaration:
            return possible_function_declaration

        possible_variable_declaration = self.__parse_variable_declaration(possible_type_token, id_token)
        if possible_variable_declaration:
            return possible_variable_declaration

        self.__consume_token(TokenType.SEMICOLON)
        return VariableDeclaration(possible_variable_declaration, id_token)

    def __parse_function_declaration(self, type_token, id_token):
        if not self.__check_token(TokenType.OPEN_BRACKET):
            return None

        arguments = self.__parse_function_declaration_arguments()
        self.__consume_token(TokenType.CLOSE_BRACKET)
        self.__consume_token(TokenType.OPEN_BLOCK)
        instructions = []
        while not self.__check_token(TokenType.CLOSE_BLOCK):
            instructions.append(self.__parse_instruction())

        return FunctionDeclaration(type_token, id_token, arguments, instructions)

    def __parse_function_declaration_arguments(self):
        possible_type_token = self.__check_if_one_of_tokens(ParserUtils.type_tokens)
        if not possible_type_token:
            return []

        id_token = self.__consume_token(TokenType.IDENTIFIER)
        arguments_so_far = [FunctionArgument(possible_type_token, id_token)]
        while self.__check_token(TokenType.COMMA):
            type_token = self.__consume_one_of_tokens(ParserUtils.type_tokens, "type token")
            id_token = self.__consume_token(TokenType.IDENTIFIER)
            arguments_so_far.append(FunctionArgument(type_token, id_token))

        return arguments_so_far

    def __parse_variable_declaration(self, possible_type_token, id_token):
        if not self.__check_token(TokenType.ASSIGN):
            return None

        value = self.__parse_r_value()
        self.__consume_token(TokenType.SEMICOLON)
        return VariableDeclaration(possible_type_token, id_token, value)

    def __parse_id_starting(self):
        possible_id_token = self.__check_token(TokenType.IDENTIFIER)
        if not possible_id_token:
            return None

        possible_assignment = self.__parse_assignment(possible_id_token)
        if possible_assignment:
            return possible_assignment

        possible_function_invocation = self.__parse_function_invocation(possible_id_token)
        if possible_function_invocation:
            return possible_function_invocation

        ParserError(self.__get_position(), f'INVALID TOKEN AFTER ID: {self.__get_current_token()}!').fatal()

    def __parse_assignment(self, id_token):
        if not self.__check_token(TokenType.ASSIGN):
            return None

        value = self.__parse_r_value()
        self.__consume_token(TokenType.SEMICOLON)

        return VariableAssignment(id_token, value)

    def __parse_r_value(self):
        return self.__parse_arithmetic_expression()  # TODO condition

    # TODO all these parse methods...
    def __parse_arithmetic_expression(self):
        pass

    def __parse_return(self):
        pass

    def __parse_while(self):
        pass

    def __parse_if(self):
        pass

    # vvv   G E T T E R S   vvv

    def __get_current_token(self):
        return self.__current_token

    def __get_next_token(self):
        self.__current_token = self.__lexer.build_and_get_token()
        return self.__current_token

    def __get_position(self):
        return self.__current_token.get_position()

    # vvv   U T I L S   vvv

    def __check_token(self, expected_token_type):
        if self.__current_token.get_type() == expected_token_type:
            token = self.__current_token
            self.__get_next_token()
            return token
        else:
            return None

    def __check_if_one_of_tokens(self, list_of_tokens_types):
        for token_type in list_of_tokens_types:
            possible_token = self.__check_token(token_type)
            if possible_token:
                return possible_token
        return None

    def __consume_token(self, expected_token_type):
        token = self.__check_token(expected_token_type)
        if token:
            return token

        ParserSyntaxError(self.__current_token.get_position(),
                          expected_token_type,
                          self.__current_token.get_type()).fatal()

    def __consume_one_of_tokens(self, list_of_tokens_types, expected_message):
        possible_token = self.__check_if_one_of_tokens(list_of_tokens_types)
        if possible_token:
            return possible_token

        ParserSyntaxError(self.__current_token.get_position(),
                          self.__current_token.get_type(),
                          expected_message).fatal()
