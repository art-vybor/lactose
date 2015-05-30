import unittest
from tempfile import mkstemp
from lactose.compiler import get_ast_tree, compile_to_string


def reduce_spaces(string):
    return string.replace(' ', '').replace('\n','')

def compile_from_string_to_string(string):
    ast_tree = get_ast_tree(string=string)
    return compile_to_string(ast_tree)

def get_lactose_program(string):
    return '#lang r5rs\n' + string + 'main'


def test(self, tests):
    for lactose, scheme in tests.iteritems():
        scheme_generated = compile_from_string_to_string(lactose)
        #print scheme_generated
        self.assertEqual(reduce_spaces(scheme_generated), reduce_spaces(scheme))


class ExpressionTest(unittest.TestCase):
    def test_tokens(self):
        tests = {'def main = #t':      '#lang r5rs\n(define (main) #t)',
                 'def main = 1':       '#lang r5rs\n(define (main) 1)',
                 'def main = #b00':    '#lang r5rs\n(define (main) #b00)',
                 #'def main = x':    '#lang r5rs\n(define (main) (x))',
        }
        test(self, tests)

    def test_precedence(self):
        tests = {'def main = 2+2':      '#lang r5rs\n(define (main) (+ 2 2))',
                 'def main = 2+2*2':       '#lang r5rs\n(define (main) (+ 2 (* 2 2)))',
                 'def main = (2+2)*2':    '#lang r5rs\n(define (main) (* (+ 2 2) 2))',
                 'def main = ((2+2)*2)':    '#lang r5rs\n(define (main) (* (+ 2 2) 2))',
                 #'def main = x*y':    '#lang r5rs\n(define (main) (* (x) (y)))',
                 #'def main = x+y':    '#lang r5rs\n(define (main) (+ (x) (y)))',
        }
        test(self, tests)        

    def test_condition(self):
        tests = {'def main = if #t then 1 else 2':
                    '#lang r5rs\n(define (main) (if #t 1 2))',
                 'def main = if 2 == 3 then 1 - 1  else sin 1':
                    '#lang r5rs\n(define (main) (if (eq? 2 3) (-1 1) (sin 1)))',
        }
        test(self, tests)
    
    def test_function_define(self):
        tests = {'def f = 1': '#lang r5rs\n(define (f) 1)',
                 'def f = 1;2': '#lang r5rs\n(define (f) 1 2)',
                 'def f x y = x+y**2': '#lang r5rs\n(define (f x y) (+ (x) (expt y 2)))',

        }
        test(self, tests)

def main():
    unittest.main()
