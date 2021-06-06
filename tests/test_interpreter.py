import io
import unittest
from unittest.mock import patch

from src.lexer.source import Source
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic_analyzer.semantic_analyzer import SemanticAnalyzer
from src.interpreter.visitor import Visitor
from src.interpreter.interpreter import Interpreter


class InterpreterTest(unittest.TestCase):
    def test_example_1(self):
        input_str = """
        
        int main(){
            int n = 8;
            if (n <= 2){
                return 1;
            }
        
            int prev = 1;
            int result = 1;
            int i = 0;
        
            while (i < n-2) {
                result = result + prev;
                prev = result - prev;
                i = i + 1;
            }
            return result;
        }"""

        expected_result = "21"

        with patch('sys.stdout', new=io.StringIO()) as temp_out:
            init_interpreter_for_test(input_str)
            self.assertEqual(temp_out.getvalue(), "RETURN: " + expected_result + "\n")

    def test_example_2(self):
        input_str = """
        
        lint main() {
            lint nums = [1, 2, 3, 4, 5];
            lint nums2 = [6, 7, 8];
        
            nums = nums + nums2;
        
            lint res = [n*n for n in nums];
            return !res;
        }"""

        expected_result = "[64, 49, 36, 25, 16, 9, 4, 1]"

        with patch('sys.stdout', new=io.StringIO()) as temp_out:
            init_interpreter_for_test(input_str)
            self.assertEqual(temp_out.getvalue(), "RETURN: " + expected_result + "\n")

    def test_example_3(self):
        input_str = """

        int main(){
            lstring a = ["Hello","world"];
            lstring b = [s + " " for s in a];
        
            b = a + b;
        
            return _b;
        }"""

        expected_result = "4"

        with patch('sys.stdout', new=io.StringIO()) as temp_out:
            init_interpreter_for_test(input_str)
            self.assertEqual(temp_out.getvalue(), "RETURN: " + expected_result + "\n")


if __name__ == '__main__':
    unittest.main()


def init_interpreter_for_test(test_string):
    source = Source(io.StringIO(test_string))
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    semantic_analyzer = SemanticAnalyzer()
    visitor = Visitor()
    analyzed_program = semantic_analyzer.start_analysis(program)
    interpreter = Interpreter(analyzed_program, visitor)
    interpreter.run()
