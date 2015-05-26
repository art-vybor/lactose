class LispTree():
    def __init__(self, ast_tree):
        self.tree = self.parse(ast_tree.root)

    # parse: function_define*;
    def parse(self, node):
        assert node.name == 'parse'

        return [self.parse_function_define(child) for child in node.children]

    # function_define: function_define_by_lambda | function_define_default;
    # function_define_by_lambda: IDENTIFIER '=' lambda_function;
    # function_define_default: IDENTIFIER function_arguments '=' function_body;
    def parse_function_define(self, node):
        assert node.name == 'function_define'

        child = node.children[0]
        name = self.parse_IDENTIFIER(child.children[0])

        if child.name == 'function_define_by_lambda':
            lambda_function = self.parse_lambda_function(child.children[2])
            return ['define', name, lambda_function]
        else: # function_define_default
            arguments = self.parse_function_arguments(child.children[1])
            body = self.parse_function_body(child.children[3])
            return ['define', [name]+arguments, body]            

    # lambda_function: '(' lambda_function ')' | '\\' function_arguments '->' function_body;
    def parse_lambda_function(self, node):
        assert node.name == 'lambda_function'

        if node.children[0] == '(': 
            return self.parse_lambda_function(node.children[1])

        arguments = self.parse_function_arguments(node.children[1])
        body = self.parse_function_body(node.children[3])

        return ['lambda', arguments] + body
    
    # function_arguments: IDENTIFIER*;
    def parse_function_arguments(self, node):
        assert node.name == 'function_arguments'

        return [self.parse_IDENTIFIER(child) for child in node.children]

    # function_body: function_body_token (';' function_body_token)*;
    # function_body_token: function_define | expression;
    def parse_function_body(self, node):
        assert node.name == 'function_body'
        function_body = []
        for child in node.children:
            if child.name == 'function_body_token':
                subchild = child.children[0]
                if subchild.name == 'function_define':
                    function_body.append(self.parse_function_define(subchild))
                else: # expression
                    function_body.append(self.parse_expression(subchild))
        return function_body

    def parse_IDENTIFIER(self, node):
        assert node.name == 'IDENTIFIER'
        return 'identifier'

    def parse_expression(self, node):
        assert node.name == 'expression'
        return 'expression'

    # def parse_function(self, ast_tree):
    #     children = ast_tree.children

    #     function = ['define']
    #     function_header = [self.parse_token(children[0])] #name
    #     function_header.extend(self.parse_function_arguments(children[1]))
    #     function.append(function_header)
    #     function.append(self.parse_function_body(children[2]))
        
    #     return function

    # def parse_function_arguments(self, ast_tree):
    #     return [self.parse_token(argument) for argument in ast_tree.children]

    # def parse_function_body(self, ast_tree):
    #     children = ast_tree.children

    #     function_body = ['cond']
    #     for branch in ast_tree.children:
    #         function_body.append(self.parse_function_branch(branch))

    #     return function_body

    # def parse_function_branch(self, ast_tree):
    #     children = ast_tree.children

    #     function_branch = []
    #     function_branch.append(self.parse_expression(children[1])) #before '='
    #     function_branch.append(self.parse_expression(children[3])) #after '='

    #     return function_branch

    # def parse_expression(self, ast_tree):
    #     children = ast_tree.children

    #     if len(children) == 1:
    #         if children[0].name == 'token':
    #             return self.parse_token(children[0])
    #         # if children[0].name == 'function_call':
    #         #     return self.parse_function_call(children[0])
    #     elif len(children) == 3 and children[0].text == '(' and children[2].text == ')':
    #         return self.parse_expression(children[1])

    #     expression = []
    #     terminals = filter(lambda x: x.terminal, children)
    #     nonterminals = filter(lambda x: not x.terminal, children)

    #     if len(terminals) == 1: #expression func
    #         expression.append(map_expression_function[terminals[0].text])
    #         #print expression
    #     else:
    #         print 'ERROR: undefined symbol in expression: %s' % terminals[0].text

    #     for nonterminal in nonterminals:
    #         expression.append(self.parse_expression(nonterminal))

    #     return expression

    # def parse_function_call(self, ast_tree):
    #     children = ast_tree.children

    #     # if len(children) == 1:
    #     #     return self.parse_token(children[1])
    #     function_call = []
    #     function_call.append(self.parse_token(children[1]))
    #     for child in children[2:-1]:
    #         if not child.terminal:
    #             function_call.append(self.parse_expression(child))
    #     return function_call


    # def parse_token(self, ast_tree):
    #     return ast_tree.children[0].text

    def tree_to_str(self, tree, root=True):
        result = ''

        if not root: result += ' ( '

        for element in tree:
            if isinstance(element, list):
                result += ' ' +  self.tree_to_str(element, False) + ' '
            else:
                result += ' ' + element + ' '

        if not root: result += ' ) '

        return ' '.join(result.split())

    def __str__(self):
        return self.tree_to_str(self.tree)


map_expression_function = {'*': '*', '/': '/', '+': '+', '-': '-', 
                           '<': '<', '<=': '<=', '>': '>', '>=': '>=',
                            '==': '=',
}