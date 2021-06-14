import sys

from src.lexer.source import Source
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic_analyzer.semantic_analyzer import SemanticAnalyzer
from src.interpreter.visitor import Visitor
from src.interpreter.interpreter import Interpreter


def init_all(input_file):
    # open the file
    file = open(input_file, "r")

    # init Source
    source = Source(file)

    # init Lexer
    lexer = Lexer(source)

    # init Parser
    parser = Parser(lexer)

    # build AST nodes
    program = parser.parse_program()

    # init Semantic Analyzer
    semantic_analyzer = SemanticAnalyzer()

    # analyze the built AST nodes
    analyzed_program = semantic_analyzer.start_analysis(program)

    # init Visitor and Interpreter
    visitor = Visitor()
    interpreter = Interpreter(analyzed_program, visitor)

    # run interpreter
    interpreter.run()


def main():
    if len(sys.argv) < 2:
        print("You have to specify input file name")
        return

    init_all(sys.argv[1])


if __name__ == "__main__":
    main()
