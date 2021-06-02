import sys

from src.lexer.source import Source
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic_analyzer.semantic_analyzer import SemanticAnalyzer


def init_all(input_file):
    file = open(input_file, "r")
    source = Source(file)
    lexer = Lexer(source)
    semantic_analyzer = SemanticAnalyzer()
    # token = lexer.build_and_get_token()
    # while token.get_type() != TokenType.EOF_SYMBOL:
    #     # for now I just print found tokens on screen
    #     print(token)
    #     token = lexer.build_and_get_token()
    parser = Parser(lexer)
    program = parser.parse_program()
    analyzed_program = semantic_analyzer.start_analysis(program)


def main():
    if len(sys.argv) < 2:
        print("You have to specify input file name")
        return

    init_all(sys.argv[1])


if __name__ == "__main__":
    main()
