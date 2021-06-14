import io
import unittest

from src.lexer.source import Source
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic_analyzer.semantic_analyzer import SemanticAnalyzer


class SemanticAnalyzerTest(unittest.TestCase):
    def test_variable_redeclaration(self):
        input_str = """
        int main(){
            int i = 4;
            int i = 5;
            return i;
        }"""
        with self.assertRaises(Exception):
            init_semantic_analyzer_for_test(input_str)

    def test_assign_invalid_type(self):
        input_str = """
        int main(){
            int i = 4;
            i = "Hey";
            return i;
        }"""
        with self.assertRaises(Exception):
            init_semantic_analyzer_for_test(input_str)

    def test_function_without_return(self):
        input_str = """
        int main(){
            int i = 4;
        }"""
        with self.assertRaises(Exception):
            init_semantic_analyzer_for_test(input_str)

    def test_return_outside_function(self):
        input_str = """
        int main(){
            int i = 4;
        }
        return i;"""
        with self.assertRaises(Exception):
            init_semantic_analyzer_for_test(input_str)

    def test_assign_undeclared_variable(self):
        input_str = """
        int main(){
            i = 4;
            return i;
        }
        """
        with self.assertRaises(Exception):
            init_semantic_analyzer_for_test(input_str)

    def test_type_mismatch_in_arithmetic_expression(self):
        input_str = """
        int main(){
            i = 4;
            float n = 2 * i;
            return i;
        }
        """
        with self.assertRaises(Exception):
            init_semantic_analyzer_for_test(input_str)

    def test_invocation_of_non_existent_function(self):
        input_str = """
        int main(){
            i = 4;
            float n = 2 * i;
            return foo(i, n);
        }
        """
        with self.assertRaises(Exception):
            init_semantic_analyzer_for_test(input_str)

    def test_invalid_number_of_args_in_function_invocation(self):
        input_str = """
        int main(){
            int foo(int a, float b, string c){
                if(_c > 5){return a;}
                else{return b;}    
            }
            i = 4;
            float n = 2 * i;
            return foo(i, n);
        }
        """
        with self.assertRaises(Exception):
            init_semantic_analyzer_for_test(input_str)

    def test_invalid_type_of_arg_in_function_invocation(self):
        input_str = """
        int main(){
            int foo(int a, float b, string c){
                if(_c > 5){return a;}
                else{return b;}    
            }
            i = 4;
            float n = 2 * i;
            string s = "Hey";
            return foo(s, i, n);
        }
        """
        with self.assertRaises(Exception):
            init_semantic_analyzer_for_test(input_str)


if __name__ == '__main__':
    unittest.main()


def init_semantic_analyzer_for_test(test_string):
    source = Source(io.StringIO(test_string))
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.start_analysis(program)
