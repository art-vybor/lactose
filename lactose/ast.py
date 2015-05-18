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

    def __str__(self):
        if self.terminal:
            return "{TYPE} '{TEXT}'".format(TYPE=self.name, TEXT=self.text)
        else:
            return self.name

    def add(self, child):
        self.children.append(child)


class AST:
    def __init__(self, antlr_tree):
        self.root = self.parse(antlr_tree)
        print map(str, self.root.children)

    def parse(self, antlr_tree):
        index = 0
        root = ASTNode(index=index)
        stack = [(root, antlr_tree)]

        while stack:
            ast_node, node = stack.pop()
            ast_node.name = lactoseParser.ruleNames[node.getRuleIndex()]

            for child in node.children:
                index += 1
                ast_child = ASTNode(index=index)
                ast_node.add(ast_child)

                if 'symbol' in child.__dict__: # is terminal
                    ast_child.terminal = True
                    ast_child.text, _ = escape_encode(str(child.getSymbol().text))
                    ast_child.name = lactoseParser.symbolicNames[child.getSymbol().type]
                else:
                    stack.append((ast_child, child))
        return root

    def print_to_console(self):
        def print_node(node, spaces=0):
            print ' '*spaces + str(node)
            for child in node.children:
                print_node(child, spaces+4)
    
        print_node(self.root)

    def print_to_dot_file(self, dot_filename):
        def get_node_name(index):
            return 'n%s' % index

        def create_node(index, label):
            label, _ = escape_encode(label.encode('utf-8'))
            return '\t{NAME} [label="{LABEL}"];\n'.format(NAME=get_node_name(index), LABEL=label)

        def create_connection(node_index, child_index):
            return '\t{NODE_NAME} -> {CHILD_NAME};\n'.format(NODE_NAME=get_node_name(node_index), 
                                                             CHILD_NAME=get_node_name(child_index))

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
