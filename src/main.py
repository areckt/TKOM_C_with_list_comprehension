import sys

from src.lexer.source import Source
from src.lexer.lexer import Lexer
from src.lexer.token import TokenType


def init_all(input_file):
    file = open(input_file, "r")
    source = Source(file)
    lexer = Lexer(source)
    # print("init_all here!")
    token = lexer.build_and_get_token()
    while token.get_type() != TokenType.EOF_SYMBOL:
        # for now I just print found tokens on screen
        print(token)
        token = lexer.build_and_get_token()


def main():
    if len(sys.argv) < 2:
        print("You have to specify input file name")
        return

    init_all(sys.argv[1])


if __name__ == "__main__":
    main()
