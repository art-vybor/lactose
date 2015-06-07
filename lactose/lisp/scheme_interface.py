
def scheme_operation(operation):
    if operation in python_to_scheme_operation:
        return python_to_scheme_operation[operation]
    return operation


python_to_scheme_operation = {
        '==': 'eq?',
        '!=': '(lambda (x y) (not (eq? x y)))',
        '**': 'expt',
        '%':  'remainder',
        '//': '(lambda (x y) (truncate (/ x y)))',
        '&':  'bitwise-and',
        '|':  'bitwise-ior',
        '^':  'bitwise-xor',
        '~':  'bitwise-not',
        '<<': 'arithmetic-shift',
        '>>': '(lambda (x y) (arithmetic-shift x (- y)))',
    }


default_symbol_table = {
    'sin':['x'],
    'main':[],
    'display':['x'],
    'newline':[],
    'sqrt':['x'],
    'floor':['x'],
    'write':['']
}