from src.error_handling import LexerError
from src.lexer.token import TokenType, Token, TokenDicts


class Lexer:
    def __init__(self, source):
        self.__source = source
        self.token = None

    def get_token(self):
        return self.token

    # #####################
    # vvv H E L P E R S vvv
    # #####################

    def __ignore_whites_and_comments(self):
        curr_char = self.__get_char()

        # consts
        WHITES = [' ', '\t', '\n']
        COMMENT = '#'

        # flags
        is_comment, is_white = False, False

        if curr_char in WHITES:
            is_white = True
        elif curr_char == COMMENT:
            is_comment = True

        # skip chars until no more comments or whites
        while is_comment or is_white:
            if is_comment:
                while curr_char != '\n':
                    curr_char = self.__move_and_get_char()
                is_comment = False
                is_white = True
            if is_white:
                while curr_char in WHITES:
                    curr_char = self.__move_and_get_char()
                is_white = False
            if curr_char == COMMENT:
                is_comment = True

    def __read_word(self):
        current_word = ""
        new_char = self.__get_char()
        if new_char.isalpha():
            while new_char.isalpha() or new_char.isdigit():
                current_word += new_char
                new_char = self.__move_and_get_char()

        return current_word

    def __move_pointer(self):
        # '_' means we don't care about the returned value
        _ = self.__source.move_and_get_char()

    def __move_and_get_char(self):
        return self.__source.move_and_get_char()

    def __get_char(self):
        return self.__source.get_char()

    def __get_position(self):
        return self.__source.get_position()

    # #####################
    # ^^^ H E L P E R S ^^^
    # #####################

    def build_and_get_token(self):
        self.__ignore_whites_and_comments()
        line, column = self.__get_position()
        token = self.__try_match()
        token.column = column
        token.line = line
        self.token = token
        return self.token

    def __try_match(self):
        return self.__try_eof() or \
            self.__try_id_or_keyword() or \
            self.__try_number() or \
            self.__try_string() or \
            self.__try_operators() or \
            self.__get_unknown_and_move()

    # try methods
    def __try_eof(self):
        if self.__get_char() == '':
            return Token(TokenType.EOF_SYMBOL)
        return None

    def __try_id_or_keyword(self):
        candidate = self.__read_word()
        if candidate in TokenDicts.keywords:
            token_type = TokenDicts.keywords[candidate]
            return Token(token_type)
        elif candidate and '[' not in candidate:
            return Token(TokenType.IDENTIFIER, candidate)
        elif candidate and '[' in candidate:
            return Token(TokenType.UNKNOWN, candidate)
        return None

    def __handle_invalid_float(self, value):
        point_position = self.__get_position()
        digit_candidate = self.__move_and_get_char()
        while digit_candidate and digit_candidate not in TokenDicts.allowed_after_number:
            value += str(digit_candidate)
            digit_candidate = self.__move_and_get_char()
        LexerError(point_position, "float number has at least 2 points and/or other bad characters").warning()
        return Token(TokenType.UNKNOWN, value)

    def __try_number(self):
        value = 0
        digit_candidate = self.__get_char()
        if digit_candidate.isdigit():

            # if we have number in range [0, 1)
            if digit_candidate == '0':
                digit_candidate = self.__move_and_get_char()
                if digit_candidate != '.':
                    return Token(TokenType.INT_LITERAL, 0)
                else:
                    _, point_position = self.__get_position()
                    digit_candidate = self.__move_and_get_char()
                    while digit_candidate.isdigit():
                        value = value * 10 + int(digit_candidate)
                        digit_candidate = self.__move_and_get_char()
                    _, current_column = self.__get_position()

                    # if there's second point
                    if digit_candidate == '.':
                        value = '0' + '.' + str(value) + '.'
                        return self.__handle_invalid_float(value)

                    return Token(TokenType.FLOAT_LITERAL, value * 10**(point_position - current_column + 1))

            # if we have number >= 1
            value = int(digit_candidate)
            digit_candidate = self.__move_and_get_char()
            while digit_candidate.isdigit():
                value = value * 10 + int(digit_candidate)
                digit_candidate = self.__move_and_get_char()
            # if there's a point we have float
            if digit_candidate == '.':
                _, point_position = self.__get_position()
                digit_candidate = self.__move_and_get_char()
                while digit_candidate.isdigit():
                    value = value * 10 + int(digit_candidate)
                    digit_candidate = self.__move_and_get_char()
                _, current_column = self.__get_position()

                # if there's second point
                if digit_candidate == '.':
                    value = value * 10**(point_position - current_column + 1)
                    value = str(value) + '.'
                    return self.__handle_invalid_float(value)

                return Token(TokenType.FLOAT_LITERAL, value * 10**(point_position - current_column + 1))

            # if there isn't a point we have int
            else:
                return Token(TokenType.INT_LITERAL, value)
        return None

    def __try_string(self):
        curr_char = self.__get_char()
        position = self.__get_position()
        if curr_char == '"':
            string = ''
            prev_char = curr_char
            curr_char = self.__move_and_get_char()
            while not(curr_char == '"' and prev_char != "\\"):
                string += curr_char
                prev_char = curr_char
                curr_char = self.__move_and_get_char()
                if prev_char == "\\":
                    if curr_char == 'n':
                        string = string[:-1]
                        string += '\n'
                        prev_char = curr_char
                        curr_char = self.__move_and_get_char()
                    elif curr_char == 't':
                        string = string[:-1]
                        string += '\t'
                        prev_char = curr_char
                        curr_char = self.__move_and_get_char()
                    elif curr_char == '\\':
                        string = string[:-1]
                        string += '\\'
                        prev_char = None
                        curr_char = self.__move_and_get_char()
                    elif curr_char == '"':
                        string = string[:-1]
                        string += '"'
                        prev_char = curr_char
                        curr_char = self.__move_and_get_char()
                if curr_char == "":
                    # if there's no closing quotation mark
                    LexerError(position, "You forgot about closing quotation mark!").warning()
                    return Token(TokenType.UNKNOWN)

            self.__move_pointer()  # move to skip '"' quote
            return Token(TokenType.STRING_LITERAL, string)
        return None

    def __try_operators(self):
        temp_token = None
        candidate = self.__get_char()
        if candidate in TokenDicts.one_char_tokens:
            temp_token_type = TokenDicts.one_char_tokens[candidate]
            temp_token = Token(temp_token_type)

        candidate += self.__move_and_get_char()
        if candidate in TokenDicts.two_char_tokens:
            temp_token_type = TokenDicts.two_char_tokens[candidate]
            temp_token = Token(temp_token_type)
            self.__move_pointer()
        return temp_token

    def __get_unknown_and_move(self):
        char = self.__get_char()
        LexerError(self.__get_position(), "UNKNOWN TOKEN").warning()
        self.__move_pointer()  # move so it's possible to continue after unknown
        return Token(TokenType.UNKNOWN, char)
