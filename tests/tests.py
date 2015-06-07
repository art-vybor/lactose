import unittest
from tempfile import mkstemp
from lactose.compiler import get_ast_tree, compile_to_string


def reduce_spaces(string):
    return string.replace(' ', '')#.replace('\n','')

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
        tests = {'def main = #t': '#lang r5rs\n(define (main) #t)\n(main)',
                 'def main = 1': '#lang r5rs\n(define (main) 1)\n(main)',
                 'def main = #b00': '#lang r5rs\n(define (main) #b00)\n(main)',
        }
        test(self, tests)

    def test_strings(self):
        tests = {'def main = "123123"': '#lang r5rs\n(define (main) "123123")\n(main)',
                 'def main = "123\n123"': '#lang r5rs\n(define (main) "123\n123")\n(main)',
                 'def main = "123\\n123"': '#lang r5rs\n(define (main) "123\\n123")\n(main)',
                 'def main = "123\\"n123"': '#lang r5rs\n(define (main) "123\\"n123")\n(main)',
        }
        test(self, tests)

    def test_comments(self):
        tests = {'--def main = "123123"': '#lang r5rs\n'}
        test(self, tests)

    def test_precedence(self):
        tests = {'def main = 2+2': '#lang r5rs\n(define (main) (+ 2 2))\n(main)',
                 'def main = 2+2*2': '#lang r5rs\n(define (main) (+ 2 (* 2 2)))\n(main)',
                 'def main = (2+2)*2': '#lang r5rs\n(define (main) (* (+ 2 2) 2))\n(main)',
                 'def main = ((2+2)*2)': '#lang r5rs\n(define (main) (* (+ 2 2) 2))\n(main)',
        }
        test(self, tests)

    def test_operation(self):
        tests = {'def main = 2==2': '#lang r5rs\n(define (main) (eq? 2 2))\n(main)',
                 'def main = 2!=2': '#lang r5rs\n(define (main) ((lambda (x y) (not (eq? x y))) 2 2))\n(main)',
                 'def main = 2**2': '#lang r5rs\n(define (main) (expt 2 2))\n(main)',
                 'def main = 2%2': '#lang r5rs\n(define (main) (remainder 2 2))\n(main)',
                 'def main = 2//2': '#lang r5rs\n(define (main) ((lambda (x y) (truncate (/ x y))) 2 2))\n(main)',
                 'def main = 2&2': '#lang r5rs\n(define (main) (bitwise-and 2 2))\n(main)',
                 'def main = 2|2': '#lang r5rs\n(define (main) (bitwise-ior 2 2))\n(main)',
                 'def main = 2^2': '#lang r5rs\n(define (main) (bitwise-xor 2 2))\n(main)',
                 'def main = ~2': '#lang r5rs\n(define (main) (bitwise-not 2))\n(main)',
                 'def main = 2<<2': '#lang r5rs\n(define (main) (arithmetic-shift 2 2))\n(main)',
                 'def main = 2>>2': '#lang r5rs\n(define (main) ((lambda (x y) (arithmetic-shift x (- y))) 2 2))\n(main)',
        }
        test(self, tests)        

    def test_condition(self):
        tests = {'def main = if #t then 1 else 2':
                    '#lang r5rs\n(define (main) (if #t 1 2))\n(main)',
                 'def main = if 2 == 3 then 1 - 1  else sin 1':
                    '#lang r5rs\n(define (main) (if (eq? 2 3) (-1 1) (sin 1)))\n(main)',
        }
        test(self, tests)
    
    def test_function_define(self):
        tests = {'def f = 1': '#lang r5rs\n(define (f) 1)',
                 'def f = 1;2': '#lang r5rs\n(define (f) 1 2)',
                 'def f x = x': '#lang r5rs\n(define (f x) x)',
                 'def f x = sin x': '#lang r5rs\n(define (f x) (sin x))',
                 'def f x y = x+y': '#lang r5rs\n(define (f x y) (+ x y))',
                 'def f x y = (x+y)': '#lang r5rs\n(define (f x y) (+ x y))',
                 'def f x y = x+y**2': '#lang r5rs\n(define (f x y) (+ x (expt y 2)))',
                 'def f = \ x -> 1': '#lang r5rs\n(define (f) (lambda (x) 1))',
                 'def f n = \ x -> x + n': '#lang r5rs\n(define (f n) (lambda (x) (+ x n)))'
        }
        test(self, tests)

    def test_function_call(self):
        tests = {'def f = 1\ndef main = f': '#lang r5rs\n(define (f) 1)\n(define (main) (f))\n(main)',
                 'def f x = x\ndef main = f 1': '#lang r5rs\n(define (f x) x)\n(define (main) (f 1))\n(main)',
                 'def f x = x\ndef main = f 2+2': '#lang r5rs\n(define (f x) x)\n(define (main) (f (+ 2 2)))\n(main)',
                 'def f x = x\ndef main = f 2+2': '#lang r5rs\n(define (f x) x)\n(define (main) (f (+ 2 2)))\n(main)',         
        }
        test(self, tests)

    def test_lambda_function_call(self):
        tests = {'def main = (\->1)': '#lang r5rs\n(define (main) ((lambda () 1)))\n(main)',
                 'def main = (\ x->x) 2': '#lang r5rs\n(define (main) ((lambda (x) x) 2))\n(main)',
                 'def main = (\ x->x) (sin 1)': '#lang r5rs\n(define (main) ((lambda (x) x) (sin 1)))\n(main)',
                 'def f = 1\ndef main = (\ x->x) f': '#lang r5rs\n(define (f) 1)\n(define (main) ((lambda (x) x) (f)))\n(main)',
                 'def main = (sin 1) + ((\ x->x) 4) + 2*3': '#lang r5rs\n(define (main) (+ (+ (sin 1) ((lambda (x) x) 4)) (* 2 3)))\n(main)',
        }
        test(self, tests)

def main():
    unittest.main()

