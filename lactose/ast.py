from codecs import escape_encode
import tempfile

from subprocess import call
from lactose.grammar.lactoseParser import lactoseParser

class ASTNode:
    def __init__(self, index):
        self.index = index
        self.text = ''
        self.name = ''
        self.terminal = False
        self.children = []
        self.antlr_node = None

        self.parent = None
        self.identifier_type = None

        self.symbol_table = {}
        self.symbol = None #(symbol, args)

    def __str__(self):
        if self.terminal:
            return "{TYPE} '{TEXT}'".format(TYPE=self.name, TEXT=self.text,)
        else:
            return "{NAME}{SYMBOL}{TABLE}".format(NAME=self.name, 
                                                    SYMBOL=self.get_symbol_in_str() if self.symbol else '',
                                                    TABLE=' | table:' + str(self.symbol_table) if self.symbol_table else '')

    def get_symbol_in_str(self):
        return ' {NAME}({ARGS})'.format(NAME=self.symbol[0], ARGS=', '.join(self.symbol[1]))

    def add_symbol_to_table(self, symbol):
        name, args = symbol
        self.symbol_table[name]=args

    def add_child(self, child):
        self.children.append(child)

    def init_identifier(self):
        self.identifier_type = get_identifier_type(self)

    
class AST:
    def __init__(self, antlr_tree):
        self.root = self.parse(antlr_tree)

    def parse(self, antlr_tree):
        self.index = 0
        return self.parse_node(antlr_tree, None)

    def parse_node(self, antlr_node, parent):
        ast_node = self.get_new_ast_node()
        ast_node.antlr_node = antlr_node
        ast_node.name = self.get_ast_node_name(antlr_node)
        ast_node.terminal = self.is_terminal(antlr_node)
        ast_node.parent = parent
        
        if ast_node.terminal:
            ast_node.text, _ = escape_encode(str(antlr_node.getSymbol().text))
        else:
            if antlr_node.children:
                for child in antlr_node.children:
                    ast_node.add_child(self.parse_node(child, ast_node))

        add_symbol_table_data(ast_node)

        return ast_node

    def get_new_ast_node(self):
        ast_node = ASTNode(index=self.index)
        self.index += 1
        return ast_node

    def get_ast_node_name(self, antlr_node):
        if self.is_terminal(antlr_node):
            return lactoseParser.symbolicNames[antlr_node.getSymbol().type]
        else:
            return lactoseParser.ruleNames[antlr_node.getRuleIndex()]

    def is_terminal(self, antlr_node):
        return 'symbol' in antlr_node.__dict__

    def print_to_console(self):
        def print_node(node, spaces=0):
            print ' '*spaces + str(node) + ' - ' + 'terminal' if str(node.terminal) else ''
            for child in node.children:
                print_node(child, spaces+4)
    
        print_node(self.root)

    def print_to_dot_file(self, dot_filename):
        def get_name(index):
            return 'n%s' % index

        def create_node(index, label):
            label, _ = escape_encode(label.encode('utf-8'))
            return '\t{NAME} [label="{LABEL}"];\n'.format(NAME=get_name(index), LABEL=label)

        def create_connection(node_index, child_index):
            return '\t{NODE_NAME} -> {CHILD_NAME};\n'.format(NODE_NAME=get_name(node_index), 
                                                             CHILD_NAME=get_name(child_index))

        def print_node(node):
            out_file.write(create_node(node.index, str(node)))

            for child in node.children:
                print_node(child)
                out_file.write(create_connection(node.index, child.index))


        with open(dot_filename, 'w') as out_file:
            out_file.write('digraph lactose_program {\n')    

            print_node(self.root)

            out_file.write('}\n')

    def print_to_pdf_file(self, pdf_filename):
        _, tmp_dot_filename = tempfile.mkstemp(suffix='.dot')
    
        self.print_to_dot_file(tmp_dot_filename)

        call(['dot', '-Tpdf', tmp_dot_filename, '-o', pdf_filename])


def add_symbol_table_data(ast_node):
    #TODO: rewrite, it's awfull
    if ast_node.name in ['function_define']:
        name = ast_node.children[1].text

        function_arguments = None
        if ast_node.children[2].name == 'function_define_default':
            function_arguments = ast_node.children[2].children[0]
        elif ast_node.children[2].name == 'function_define_by_lambda':
            function_arguments = ast_node.children[2].children[1].children[1]

        args = [f_arg.text for f_arg in function_arguments.children]

        ast_node.symbol = (name, args)
    
    if ast_node.name == 'lambda_function':
        name = None
        function_arguments = ast_node.children[1]
        args = [f_arg.text for f_arg in function_arguments.children]
        ast_node.symbol = (name, args)    
              

    if ast_node.name == 'parse':
        for child in ast_node.children:
            if child.symbol:
                ast_node.add_symbol_to_table(child.symbol)

    if ast_node.name == 'function_define':
        for child in ast_node.children[-1].children[-1].children[-1].children:
            if child.symbol:
                ast_node.add_symbol_to_table(child.symbol)

    # if ast_node.name == 'lambda_function':
    #     for child in ast_node.children[1].children:
    #         ast_node.add_symbol_to_table(child.symbol)            


def get_identifier_type(node):
    identifier_text = node.text
    while node != None:
        if identifier_text in node.symbol_table:
            return ('function_call', node.symbol_table[identifier_text])
        elif node.symbol and identifier_text in node.symbol[1]:
            return ('argument',)
        node = node.parent
    return None
