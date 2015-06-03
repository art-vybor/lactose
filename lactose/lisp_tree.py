from lactose.exception.errors import IdentifierNotFoundError

class LispTree():
    def __init__(self, ast_tree):
        self.main = 'main' in ast_tree.root.symbol_table
        ast_tree.root.symbol_table.update(get_default_symbol_table())

        self.tree = self.parse(ast_tree.root)

    # parse: function_define*;
    def parse(self, node):
        assert node.name == 'parse', 'node is %s' % node
        return [self.parse_function_define(child) for child in node.children]

    # function_define: 'def' IDENTIFIER function_arguments '=' function_body;
    # function_define_default: ;
    def parse_function_define(self, node):
        assert node.name == 'function_define', 'node is %s' % node

        name = self.parse_IDENTIFIER(node.children[1])

        arguments = self.parse_function_arguments(node.children[2])
        body = self.parse_function_body(node.children[4])

        if len(arguments) == 0: name = name[0]
        return ['define', [name]+arguments]+body

    # lambda_function: '(' lambda_function ')' | '\\' function_arguments '->' function_body;
    def parse_lambda_function(self, node):
        assert node.name == 'lambda_function', 'node is %s' % node

        if node.children[0].text == '(': 
            return self.parse_lambda_function(node.children[1])

        arguments = self.parse_function_arguments(node.children[1])
        body = self.parse_function_body(node.children[3])        
        return ['lambda', arguments] + body
    
    # function_arguments: IDENTIFIER*;
    def parse_function_arguments(self, node):
        assert node.name == 'function_arguments', 'node is %s' % node
        return [self.parse_IDENTIFIER(child) for child in node.children]

    # function_body: function_body_token (';' function_body_token)*;
    # function_body_token: function_define | expression;
    def parse_function_body(self, node):
        assert node.name == 'function_body', 'node is %s' % node
        function_body = []
        for child in node.children:
            if child.name == 'function_body_token':
                subchild = child.children[0]
                if subchild.name == 'function_define':
                    function_body.append(self.parse_function_define(subchild))
                else: # expression
                    function_body.append(self.parse_expression(subchild))

        return function_body
    
    # expression 
    # : '(' expression ')' 
    # | if_condition
    # | ('+'|'-') expression
    # | ('not'|'~') expression
    # | expression '**' expression
    # | expression ('*'|'/'|'%'|'//') expression
    # | expression ('+'|'-') expression
    # | expression ('<<' | '>>') expression
    # | expression '&' expression
    # | expression '^' expression
    # | expression '|' expression
    # | expression 'and' expression
    # | expression 'or' expression
    # | expression ('<' | '<=' | '>' | '>=') expression
    # | expression ('==' | '!=') expression
    # | token
    # | IDENTIFIER
    # | lambda_function
    # | function_call
    # | lambda_function_call;
    def parse_expression(self, node):
        assert node.name == 'expression', 'node is %s' % node

        children = node.children
        if children[0].name == 'if_condition':
            return self.parse_if_condition(children[0])
        elif children[0].name == 'token':
            return self.parse_token(children[0])
        elif children[0].name == 'IDENTIFIER':
            return self.parse_IDENTIFIER(children[0])
        elif children[0].name == 'lambda_function':
            return self.parse_lambda_function(children[0])
        elif children[0].name == 'function_call':
            return self.parse_function_call(children[0])
        elif children[0].name == 'lambda_function_call':
            return self.parse_lambda_function_call(children[0])
        elif children[0].text == '(':
            return self.parse_expression(children[1])
        elif children[0].text in ['+', '-', 'not', '~']:
            # unary
            operation = get_scheme_operation(children[0].text)
            expr = self.parse_expression(children[1])
            return [operation, expr]
        else:
            # binary
            expr_1 = self.parse_expression(children[0])
            operation = get_scheme_operation(children[1].text)
            expr_2 = self.parse_expression(children[2])
            return [operation, expr_1, expr_2]

    # if_condition: 'if' expression 'then' expression 'else' expression;
    def parse_if_condition(self, node):
        assert node.name == 'if_condition', 'node is %s' % node

        expr_1 = self.parse_expression(node.children[1])
        expr_2 = self.parse_expression(node.children[3])
        expr_3 = self.parse_expression(node.children[5])
        return ['if', expr_1, expr_2, expr_3] 

    # function_call: IDENTIFIER expression*;
    def parse_function_call(self, node):
        assert node.name == 'function_call', 'node is %s' % node

        identifier = self.parse_IDENTIFIER(node.children[0])
        args = []
        for child in node.children[1:]:
            args.append(self.parse_expression(child))

        return [identifier] + args

    # lambda_function_call: '(' lambda_function ')' expression*;
    def parse_lambda_function_call(self, node):
        assert node.name == 'lambda_function_call', 'node is %s' % node

        lambda_func = self.parse_lambda_function(node.children[1])
        args = []
        for child in node.children[3:]:
            args.append(self.parse_expression(child))
        return [lambda_func] + args

    # token: IDENTIFIER | BOOLEAN | NUMBER | CHARACTER | STRING;
    def parse_token(self, node):
        assert node.name == 'token', 'node is %s' % node
        return node.children[0].text

    # IDENTIFIER
    def parse_IDENTIFIER(self, node):
        assert node.name == 'IDENTIFIER', 'node is %s' % node
        node.init_identifier()

        if not node.identifier_type:
            raise IdentifierNotFoundError(node)

        if node.identifier_type[0] == 'function_call' and len(node.identifier_type[1]) == 0:
            return [node.text]

        return node.text

    def tree_to_str(self, tree, root=True):
        def f(x):
            if isinstance(x, list):
                return self.tree_to_str(x, False)
            return x
        if not root:
            return '(' + ' '.join(map(f, tree)) + ')'
        else:
            return '\n'.join(map(f, tree)) + ('\n(main)' if self.main else '')

    def __str__(self):
        return self.tree_to_str(self.tree)


def get_scheme_operation(operation):
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

    if operation in python_to_scheme_operation:
        return python_to_scheme_operation[operation]
    return operation


def get_default_symbol_table():
    return {'sin':['x'],
            'main':[],
            'display':['x'],
            'newline':[],
            'sqrt':['x'],
            'floor':['x'],
            'write':['']}
