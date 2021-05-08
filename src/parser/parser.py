from src.error_handling import ParserError, ParserSyntaxError
from src.lexer.token import TokenType
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

    # TODO all these parse methods...
    def __parse_declaration(self):
        pass

    def __parse_id_starting(self):
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
