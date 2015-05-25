import unittest
from tempfile import mkstemp
from lactose.compiler import get_ast_tree, compile_to_string


def reduce_spaces(string):
    return string.replace(' ', '')

def compile_from_string_to_string(string):
    ast_tree = get_ast_tree(string=string)
    return compile_to_string(ast_tree)


class TestExpression(unittest.TestCase):
    def test_tokens(self):
        program = '(f #t)'
        result = '#lang r5rs\n(f #t)'
        self.assertEqual(reduce_spaces(compile_from_string_to_string(program)), reduce_spaces(result))

        program = '(f x)'
        result = '#lang r5rs\n(f x)'
        self.assertEqual(reduce_spaces(compile_from_string_to_string(program)), reduce_spaces(result))

        program = '(f -1) (f +1-2)'
        result = '#lang r5rs\n(f (- 1)) (f (-(+1)2))'
        self.assertEqual(reduce_spaces(compile_from_string_to_string(program)), reduce_spaces(result))

    def test_expressions(self):
        program = '(f 2+2)'
        result = '#lang r5rs\n(f (+2 2))'
        self.assertEqual(reduce_spaces(compile_from_string_to_string(program)), reduce_spaces(result))

        program = '(f 2+2*2)'
        result = '#lang r5rs\n(f (+ 2 (* 2 2)))'
        self.assertEqual(reduce_spaces(compile_from_string_to_string(program)), reduce_spaces(result))

        program = '(f (2+2)*2)'
        result = '#lang r5rs\n(f (* (+ 2 2) 2))'
        self.assertEqual(reduce_spaces(compile_from_string_to_string(program)), reduce_spaces(result))

def main():
    unittest.main()