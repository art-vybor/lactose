from time import time
from lactose.compiler import get_ast_tree, compile_to_string

def compile_from_string_to_string(string):
    ast_tree = get_ast_tree(string=string)
    return compile_to_string(ast_tree)


define_template = "def abs{INDEX} x = if x >= 0 then x else -x"
num_of_define = 300
step = 10
for i in range(step,num_of_define,step):
    program = '\n'.join([define_template.format(INDEX=index) for index in range(0, i)])
    start = time()
    res = compile_from_string_to_string(program)
    end = time()

    print str(i), str(end-start)