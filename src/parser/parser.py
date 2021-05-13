from src.error_handling import ParserError, ParserSyntaxError
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
            ParserError(self.__get_position(), "unknown instruction").warning()
        return possible_instruction

    def __parse_declaration(self):
        possible_type_token = self.__check_if_one_of_tokens(ParserUtils.type_tokens)
        list_type_flag = False
        if not possible_type_token:
            possible_type_token = self.__check_if_one_of_tokens(ParserUtils.list_type_tokens)
            if not possible_type_token:
                return None
            else:
                list_type_flag = True

        id_token = self.__consume_token(TokenType.IDENTIFIER)

        possible_function_declaration = self.__parse_function_declaration(possible_type_token, id_token)
        if possible_function_declaration:
            return possible_function_declaration

        if not list_type_flag:
            possible_variable_declaration = self.__parse_variable_declaration(possible_type_token, id_token)
            if possible_variable_declaration:
                return possible_variable_declaration
        else:
            possible_list_variable_declaration = self.__parse_list_variable_declaration(possible_type_token, id_token)
            if possible_list_variable_declaration:
                return possible_list_variable_declaration

        ParserError(self.__get_position(), "declaration error").fatal()

        # self.__consume_token(TokenType.SEMICOLON)
        # return VariableDeclaration(possible_type_token, id_token)

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

    def __parse_list_variable_declaration(self, possible_type_token, id_token):
        if not self.__check_token(TokenType.ASSIGN):
            return None

        self.__consume_token(TokenType.OPEN_LIST)
        value = self.__parse_arithmetic_expression()
        if value is None:
            self.__consume_token(TokenType.CLOSE_LIST)
            self.__consume_token(TokenType.SEMICOLON)
            return ListVariableDeclaration(possible_type_token, id_token, [])
        else:
            values = [value]
            while self.__check_token(TokenType.COMMA):
                values.append(self.__parse_arithmetic_expression())

            # LIST COMPREHENSION --- check if there's 'for' keyword
            if len(values) == 1 and self.__get_current_token().get_type() == TokenType.FOR_KEYWORD:
                self.__consume_token(TokenType.FOR_KEYWORD)
                for_id = self.__parse_id_or_literal()
                self.__consume_token(TokenType.IN_KEYWORD)
                in_expression = self.__parse_arithmetic_expression()
                self.__consume_token(TokenType.CLOSE_LIST)
                self.__consume_token(TokenType.SEMICOLON)
                return ListComprehensionDeclaration(possible_type_token, id_token, value, for_id, in_expression)

            # check for errors like: lint nums = [1, 2, n*n for n in nums];
            elif len(values) > 1 and self.__get_current_token().get_type() == TokenType.FOR_KEYWORD:
                ParserError(self.__get_position(), "list comprehension error").fatal()

            self.__consume_token(TokenType.CLOSE_LIST)
            self.__consume_token(TokenType.SEMICOLON)
            return ListVariableDeclaration(possible_type_token, id_token, values)

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

        ParserError(self.__get_position(), f'invalid token after id: {self.__get_current_token()}!').fatal()

    def __parse_assignment(self, id_token):
        if not self.__check_token(TokenType.ASSIGN):
            return None

        value = self.__parse_r_value()

        if value:
            self.__consume_token(TokenType.SEMICOLON)
            return VariableAssignment(id_token, value)

        else:
            self.__consume_token(TokenType.OPEN_LIST)
            value = self.__parse_arithmetic_expression()
            values = [value]

            while self.__check_token(TokenType.COMMA):
                values.append(self.__parse_arithmetic_expression())

            # LIST COMPREHENSION --- check if there's 'for' keyword
            if len(values) == 1 and self.__get_current_token().get_type() == TokenType.FOR_KEYWORD:
                self.__consume_token(TokenType.FOR_KEYWORD)
                for_id = self.__parse_id_or_literal()
                self.__consume_token(TokenType.IN_KEYWORD)
                in_expression = self.__parse_arithmetic_expression()
                self.__consume_token(TokenType.CLOSE_LIST)
                self.__consume_token(TokenType.SEMICOLON)
                return ListComprehensionAssignment(id_token, value, for_id, in_expression)

            # check for errors like: lint nums = [1, 2, n*n for n in nums];
            elif len(values) > 1 and self.__get_current_token().get_type() == TokenType.FOR_KEYWORD:
                ParserError(self.__get_position(), "list comprehension error").fatal()

            self.__consume_token(TokenType.CLOSE_LIST)
            self.__consume_token(TokenType.SEMICOLON)
            return ListVariableAssignment(id_token, values)

    def __parse_r_value(self):
        return self.__parse_arithmetic_expression()  # TODO condition

    def __parse_arithmetic_expression(self):
        result = self.__parse_multiplicative_factor()

        if result:
            additive_token = self.__check_if_one_of_tokens(ParserUtils.additive_operator_tokens)
            while additive_token:
                result = ArithmeticExpression(result,
                                              ArithmeticOperator(additive_token),
                                              self.__parse_multiplicative_factor())
                additive_token = self.__check_if_one_of_tokens(ParserUtils.additive_operator_tokens)

        return result

    def __parse_multiplicative_factor(self):
        multiplicative_factor = self.__parse_additive_factor()

        if multiplicative_factor:
            possible_multiplicative_token = self.__check_if_one_of_tokens(ParserUtils.multiplicative_operator_tokens)
            while possible_multiplicative_token:
                multiplicative_factor = ArithmeticExpression(multiplicative_factor,
                                                             ArithmeticOperator(possible_multiplicative_token),
                                                             self.__parse_additive_factor())
                possible_multiplicative_token = self.__check_if_one_of_tokens(
                    ParserUtils.multiplicative_operator_tokens)

        return multiplicative_factor

    def __parse_additive_factor(self):
        additive_factor = self.__parse_id_or_literal()

        if not additive_factor and self.__check_token(TokenType.OPEN_BRACKET):
            additive_factor = self.__parse_arithmetic_expression()
            self.__consume_token(TokenType.CLOSE_BRACKET)

        return additive_factor

    def __parse_condition(self):
        possible_left_id_or_literal = self.__parse_id_or_literal()
        if not possible_left_id_or_literal:
            return None

        possible_comparison_token = self.__check_if_one_of_tokens(ParserUtils.comparison_tokens)
        if possible_comparison_token:
            possible_right_id_or_literal = self.__parse_id_or_literal()
            if not possible_right_id_or_literal:
                ParserError(self.__get_position(),
                            f'expected literal or id, instead got {self.__get_current_token()}').fatal()
            return SingleCondition(possible_left_id_or_literal, possible_comparison_token, possible_right_id_or_literal)
        return possible_left_id_or_literal

    def __parse_function_invocation(self, id_token):
        if not self.__check_token(TokenType.OPEN_BRACKET):
            return None

        arguments = self.__parse_function_invocation_arguments()
        self.__consume_token(TokenType.CLOSE_BRACKET)
        self.__consume_token(TokenType.SEMICOLON)

        return FunctionInvocation(id_token, arguments)

    def __parse_function_invocation_arguments(self):
        possible_argument = self.__parse_arithmetic_expression()
        if not possible_argument:
            return []

        arguments_so_far = [possible_argument]
        while self.__check_token(TokenType.COMMA):
            arguments_so_far.append(self.__parse_arithmetic_expression())

        return arguments_so_far

    def __parse_id_or_literal(self):
        possible_literal = self.__check_if_one_of_tokens(ParserUtils.literal_tokens)
        if possible_literal:
            return Literal(possible_literal)

        possible_id = self.__check_token(TokenType.IDENTIFIER)
        if possible_id:
            # check if there's [expression], e.g. nums[3], nums[i], nums[a*(2+b)/c]
            if self.__get_current_token().get_type() == TokenType.OPEN_LIST:
                self.__consume_token(TokenType.OPEN_LIST)
                index = self.__parse_arithmetic_expression()
                self.__consume_token(TokenType.CLOSE_LIST)
                return ListElement(Id(possible_id), index)
            else:
                return Id(possible_id)

        return None

    def __parse_return(self):
        if not self.__check_token(TokenType.RETURN_KEYWORD):
            return None

        possible_return_value = self.__parse_r_value()
        self.__consume_token(TokenType.SEMICOLON)

        return ReturnExpression(possible_return_value)

    def __parse_while(self):
        if not self.__check_token(TokenType.WHILE_KEYWORD):
            return None

        self.__consume_token(TokenType.OPEN_BRACKET)
        condition = self.__parse_condition()
        if condition is None:
            ParserError(self.__get_position(), 'no condition in while statement').fatal()
        self.__consume_token(TokenType.CLOSE_BRACKET)
        self.__consume_token(TokenType.OPEN_BLOCK)
        instructions = self.__parse_scope()
        return WhileStatement(condition, instructions)

    def __parse_if(self):
        if not self.__check_token(TokenType.IF_KEYWORD):
            return None

        self.__consume_token(TokenType.OPEN_BRACKET)
        condition = self.__parse_condition()
        if condition is None:
            ParserError(self.__get_position(), 'no condition in if statement').fatal()
        self.__consume_token(TokenType.CLOSE_BRACKET)
        self.__consume_token(TokenType.OPEN_BLOCK)
        if_instructions = self.__parse_scope()

        else_instructions = []
        if self.__check_token(TokenType.ELSE_KEYWORD):
            self.__consume_token(TokenType.OPEN_BLOCK)
            else_instructions = self.__parse_scope()

        return IfStatement(condition, if_instructions, else_instructions)

    def __parse_scope(self):
        scope = []
        while not self.__check_token(TokenType.CLOSE_BLOCK):
            new_instruction = self.__parse_instruction()
            scope.append(new_instruction)

        return scope

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
