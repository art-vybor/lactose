class LispTree():
    def __init__(self, ast_tree):
        self.tree = self.parse(ast_tree.root)

    def parse(self, ast_tree):
        lactose_program = []

        for child in ast_tree.children:
            parse_child = ''
            if child.name == 'function':
                parse_child = self.parse_function(child)
            elif child.name == 'expression':
                parse_child = self.parse_expression(child)
            elif child.name == 'NEWLINE':
                continue
            else:
                print 'ERROR: parse root'

            lactose_program.append(parse_child)
            
        return lactose_program

    def parse_function(self, ast_tree):
        children = ast_tree.children

        function = ['define']
        function_header = [self.parse_token(children[0])] #name
        function_header.extend(self.parse_function_arguments(children[1]))
        function.append(function_header)
        function.append(self.parse_function_body(children[2]))
        
        return function

    def parse_function_arguments(self, ast_tree):
        return [self.parse_token(argument) for argument in ast_tree.children]

    def parse_function_body(self, ast_tree):
        children = ast_tree.children

        function_body = ['cond']
        for branch in ast_tree.children:
            function_body.append(self.parse_function_branch(branch))

        return function_body

    def parse_function_branch(self, ast_tree):
        children = ast_tree.children

        function_branch = []
        function_branch.append(self.parse_expression(children[1])) #before '='
        function_branch.append(self.parse_expression(children[3])) #after '='

        return function_branch

    def parse_expression(self, ast_tree):
        children = ast_tree.children

        if len(children) == 1:
            if children[0].name == 'token':
                return self.parse_token(children[0])
            if children[0].name == 'function_call':
                return self.parse_function_call(children[0])
        elif len(children) == 3 and children[0].text == '(' and children[2].text == ')':
            return [self.parse_expression(children[1])]


        expression = []
        terminals = filter(lambda x: x.terminal, children)
        nonterminals = filter(lambda x: not x.terminal, children)

        if len(terminals) == 1: #expression func
            expression.append(map_expression_function[terminals[0].text])
        else:
            print 'ERROR: undefined symbol in expression: %s' % terminals[0].text

        for nonterminal in nonterminals:
            expression.append(self.parse_expression(nonterminal))

        return expression

    def parse_function_call(self, ast_tree):
        children = ast_tree.children

        if len(children) == 1:
            return self.parse_token(children[0])
        function_call = []
        function_call.append(self.parse_token(children[0]))
        for child in children[1:]:
            if not child.terminal:
                function_call.append(self.parse_expression(child))
        return function_call


    def parse_token(self, ast_tree):
        return ast_tree.children[0].text

    def tree_to_str(self, tree, root=True):
        result = ''

        if not root: result += '( '

        for element in tree:
            if isinstance(element, list):
                result += self.tree_to_str(element, False)
            else:
                result += element + ' '

        if not root: result += ' )'

        return result

    def __str__(self):
        return self.tree_to_str(self.tree)


map_expression_function = {'*': '*', '/': '/', '+': '+', '-': '-', 
                           '<': '<', '<=': '<=', '>': '>', '>=': '>=',
                            '==': '=',
}