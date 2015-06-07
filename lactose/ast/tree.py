import tempfile
from codecs import escape_encode
from subprocess import call

from lactose.grammar.lactoseParser import lactoseParser
from lactose.ast.symbol_table import init_symbol_table
from lactose.ast.node import ASTNode
    
class AST:
    def __init__(self, antlr_tree):
        self.root = self.parse(antlr_tree)
        init_symbol_table(self.root)

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
            ast_node.text = str(antlr_node.getSymbol().text)
        else:
            if antlr_node.children:
                for child in antlr_node.children:
                    ast_node.add_child(self.parse_node(child, ast_node))

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