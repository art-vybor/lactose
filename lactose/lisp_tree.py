class LispTree():
    def __init__(self, ast_tree):
        ast_tree.root.symbol_table.update(get_default_symbol_table())
        self.tree = self.parse(ast_tree.root)

        #print self.tree

    # parse: function_define*;
    def parse(self, node):
        assert node.name == 'parse', 'node is %s' % node

        return [self.parse_function_define(child) for child in node.children]

    # function_define: 'def' IDENTIFIER (function_define_by_lambda | function_define_default);
    # function_define_by_lambda: '=' lambda_function;
    # function_define_default: function_arguments '=' function_body;
    def parse_function_define(self, node):
        assert node.name == 'function_define', 'node is %s' % node

        name = self.parse_IDENTIFIER(node.children[1])

        child = node.children[2]
        if child.name == 'function_define_by_lambda':
            lambda_function = self.parse_lambda_function(child.children[1])
            arguments = lambda_function[1]
            if len(arguments) == 0: name = name[0]
            return ['define', name, lambda_function]
        else: # function_define_default
            arguments = self.parse_function_arguments(child.children[0])
            body = self.parse_function_body(child.children[2])

            if len(arguments) == 0: name = name[0]

            if isinstance(body, list):
                return ['define', [name]+arguments]+body
            else:
                assert False
                return ['define', [name]+arguments, body]

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

        # if len(function_body) == 1:
        #     return function_body[0]
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
        #print '%s, %s' % (node, node.identifier_type)

        if not node.identifier_type:
            raise Exception('invalid ident %s' % node)

        if node.identifier_type[0] == 'function_call' and len(node.identifier_type[1]) == 0:
            return [node.text]

        return node.text

    def tree_to_str(self, tree, root=True):
        def f(x):
            if isinstance(x, list):
                return self.tree_to_str(x, False)
            return x
        return '(' + ' '.join(map(f, tree)) + ')' if not root else '\n'.join(map(f, tree))

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
    return {'sin':['x'], 'main':[]}
