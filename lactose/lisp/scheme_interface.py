
def scheme_operation(operation):
    if operation in python_to_scheme_operation:
        return python_to_scheme_operation[operation]
    return operation


python_to_scheme_operation = {
        '==': '=',
        '!=': '(lambda (x y) (not (= x y)))',
        '**': 'expt',
        '%': 'remainder',
        '//': '(lambda (x y) (truncate (/ x y)))',
        '&': 'bitwise-and',
        '|': 'bitwise-ior',
        '^': 'bitwise-xor',
        '~': 'bitwise-not',
        '<<': 'arithmetic-shift',
        '>>': '(lambda (x y) (arithmetic-shift x (- y)))',
    }

def scheme_function(function):
    if function in lactose_to_scheme_function:
        return lactose_to_scheme_function[function]
    return function

lactose_to_scheme_function = {
    'len': 'length',
    'concat': 'append',
    'tail': 'list-tail',    
    'take': """((lambda (f)
                 (lambda (x y)
                   (f f x y)))
               (lambda (head l n)
                 (if (= n 0)
                     '()
                     (cons (car l) (head head (cdr l) (- n 1))))))""",
    'ref': 'list-ref',
}

default_symbol_table = {
    'main':[],
    # math
    'sin':['x'],
    'floor':['x'],
    'sqrt':['x'],

    # io
    'display':['x'],
    'newline':[],    
    'write':['x'],
    'read':[],

    # lists
    'len': ['lst'],
    'concat': ['lst', '...'],
    'tail': ['lst', 'pos'],
    'take': ['lst', 'pos'],    
    'ref': ['lst', 'pos'],
    'reverse': ['lst'],
}

