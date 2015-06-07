from lactose.exception.errors import IdentifierNotFoundError
from lactose.lisp.scheme_interface import scheme_operation, default_symbol_table
from lactose.ast.symbol_table import get_identifier_type

class LispTree():
    def __init__(self, ast_tree):
        self.main = 'main' in ast_tree.root.symbol_table
        self.errors = 0

        ast_tree.root.symbol_table.update(default_symbol_table)

        self.tree = self.parse(ast_tree.root)

    # parse: function_define*;
    def parse(self, node):
        self.node_assert(node, 'parse')
        return [self.parse_function_define(child) for child in node.children]

    # function_define: 'def' IDENTIFIER function_arguments '=' (function_body | '{' function_body '}');
    def parse_function_define(self, node):
        self.node_assert(node, 'function_define')

        name = self.parse_IDENTIFIER(node.children[1])

        arguments = self.parse_function_arguments(node.children[2])

        if node.children[-1].text == '}':
            body = self.parse_function_body(node.children[5])
        else:
            body = self.parse_function_body(node.children[4])

        if len(arguments) == 0: name = name[0] # kludge for fix IDENTIFIER and function_call priority

        return ['define', [name]+arguments]+body

    # lambda_function: '\\' function_arguments '->' function_body;
    def parse_lambda_function(self, node):
        self.node_assert(node, 'lambda_function')

        arguments = self.parse_function_arguments(node.children[1])
        body = self.parse_function_body(node.children[3])        
        return ['lambda', arguments] + body
    
    # function_arguments: IDENTIFIER*;
    def parse_function_arguments(self, node):
        self.node_assert(node, 'function_arguments')
        return [self.parse_IDENTIFIER(child) for child in node.children]

    # function_body: function_body_token (';' function_body_token)*;
    # function_body_token: function_define | expression;
    def parse_function_body(self, node):
        self.node_assert(node, 'function_body')

        function_body = []
        for child in node.children:
            if child.name == 'function_body_token':
                token = child.children[0]
                if token.name == 'expression':
                    function_body.append(self.parse_expression(token))
                elif token.name == 'function_define':
                    function_body.append(self.parse_function_define(token))

        return function_body
    
    # expression 
    #     : expression '**' expression
    #     | expression ('*'|'/'|'%'|'//') expression
    #     | expression ('+'|'-') expression
    #     | expression ('<<' | '>>') expression
    #     | expression '&' expression
    #     | expression '^' expression
    #     | expression '|' expression
    #     | expression 'and' expression
    #     | expression 'or' expression
    #     | expression ('<' | '<=' | '>' | '>=') expression
    #     | expression ('==' | '!=') expression
    #     | ('+'|'-') expression
    #     | ('not'|'~') expression
    #     | if_condition
    #     | token
    #     | IDENTIFIER
    #     | lambda_function
    #     | function_call
    #     | lambda_function_call    
    #     | '(' expression ')' 
    #     | list_expression
    #     ;
    def parse_expression(self, node):
        self.node_assert(node, 'expression')

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
        elif children[0].name == 'list_expression':
            return self.parse_list_expression(children[0])
        elif children[0].text == '(':
            return self.parse_expression(children[1])
        elif children[0].text in ['+', '-', 'not', '~']:
            # unary
            operation = scheme_operation(children[0].text)
            expr = self.parse_expression(children[1])
            return [operation, expr]
        else:
            # binary
            expr_1 = self.parse_expression(children[0])
            operation = scheme_operation(children[1].text)
            expr_2 = self.parse_expression(children[2])
            return [operation, expr_1, expr_2]

    # if_condition: 'if' expression 'then' expression 'else' expression;
    def parse_if_condition(self, node):
        self.node_assert(node, 'if_condition')

        expr_1 = self.parse_expression(node.children[1])
        expr_2 = self.parse_expression(node.children[3])
        expr_3 = self.parse_expression(node.children[5])
        return ['if', expr_1, expr_2, expr_3] 

    # function_call: IDENTIFIER expression*;
    def parse_function_call(self, node):
        self.node_assert(node, 'function_call')

        identifier = self.parse_IDENTIFIER(node.children[0])
        args = []
        for child in node.children[1:]:
            args.append(self.parse_expression(child))

        return [identifier] + args

    # lambda_function_call: '(' lambda_function ')' expression*;
    def parse_lambda_function_call(self, node):
        self.node_assert(node, 'lambda_function_call')

        lambda_func = self.parse_lambda_function(node.children[1])
        args = []
        for child in node.children[3:]:
            args.append(self.parse_expression(child))
        return [lambda_func] + args

    #list_expression: '[' expression* ']';
    def parse_list_expression(self, node):
        self.node_assert(node, 'list_expression')

    # token: BOOLEAN | NUMBER | CHARACTER | STRING;
    def parse_token(self, node):
        self.node_assert(node, 'token')
        return node.children[0].text

    # IDENTIFIER
    def parse_IDENTIFIER(self, node):
        self.node_assert(node, 'IDENTIFIER')

        ident_type = get_identifier_type(node)

        if not ident_type:
            self.errors += 1
            print IdentifierNotFoundError(node)

        # kludge for fix IDENTIFIER and function_call priority
        if ident_type[0] == 'function_call' and len(ident_type[1]) == 0:
            return [node.text]

        return node.text

    def node_assert(self, node, expected_type):
        assert node.name == expected_type, 'Node is %s, but %s expected.' % (node, expected_type)

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
