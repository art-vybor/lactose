import unittest
from tempfile import mkstemp
from lactose.compiler import get_ast_tree, compile_to_string


def compile_from_string_to_string(string):
    ast_tree = get_ast_tree(string=string)
    return compile_to_string(ast_tree)


class TestCompiler(unittest.TestCase):
    def test_f(self):
        program = 'sign x | #t = 10\n'
        result = '#lang r5rs\n( define ( sign x  )( cond ( #t 10  ) ) )'
        self.assertEqual(compile_from_string_to_string(program), result)

        

def main():
    unittest.main()