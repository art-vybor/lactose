def init_symbol_table(ast_node):
    add_symbol_information(ast_node)

    if ast_node.children:
        for child in ast_node.children:
            init_symbol_table(child)

    add_symbols_to_table(ast_node)


def add_symbol_information(ast_node):
    def get_symbol(name, ast_function_arguments):
        return (name, [arg.text for arg in ast_function_arguments.children])

    # function_define: 'def' IDENTIFIER function_arguments '=' (function_body | '{' function_body '}'); 
    if ast_node.name == 'function_define':
        ast_node.symbol = get_symbol(ast_node.children[1].text, ast_node.children[2])

    # lambda_function: '\\' function_arguments '->' function_body;
    if ast_node.name == 'lambda_function':
        ast_node.symbol = get_symbol(None, ast_node.children[1])


def add_symbols_to_table(ast_node):
    #parse: function_define*;
    if ast_node.name == 'parse':
        for function_define in ast_node.children:
            ast_node.add_symbol_to_table(function_define.symbol)

    # function_define: 'def' IDENTIFIER function_arguments '=' (function_body | '{' function_body '}'); 
    # function_body: function_body_token (';' function_body_token)*;
    # function_body_token: function_define | expression;
    if ast_node.name == 'function_define':
        function_body = ast_node.children[-1]
        if function_body.text == '}':
            function_body = ast_node.children[-2]

        print map(lambda x: x.symbol, function_body.children)

        for child in function_body.children: #child is unction_body_token or ';'
            if child.children and child.children[0].name == 'function_define': 
                ast_node.add_symbol_to_table(child.children[0].symbol)


def get_identifier_type(node):
    identifier_text = node.text
    while node != None:
        if identifier_text in node.symbol_table:
            return ('function_call', node.symbol_table[identifier_text])
        elif node.symbol and identifier_text in node.symbol[1]:
            return ('argument',)
        node = node.parent
    return None