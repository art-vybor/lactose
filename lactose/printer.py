from codecs import escape_encode
import tempfile

from subprocess import call
from lactose.grammar.lactoseParser import lactoseParser

def get_tree_structure(tree):
    

    index = 0
    tree_structure = {'index': index, 'children': []}
    q = [(tree_structure, tree)]

    while q:
        node_structure, node = q.pop()
        node_structure['label'] = lactoseParser.ruleNames[node.getRuleIndex()]

        for child in node.children:
            index += 1
            child_structure = {'index': index, 'children': []}

            node_structure['children'].append(child_structure)

            if 'symbol' in child.__dict__:
                text, _ = escape_encode(str(child.getSymbol().text))

                child_structure['label'] = "{TYPE} '{TEXT}'".format(
                                                TYPE=lactoseParser.symbolicNames[child.getSymbol().type], TEXT=text)
            else:
                q.append((child_structure, child))

    return tree_structure


def print_tree_structure_to_console(tree):
    def print_node(node, spaces=0):
        print ' '*spaces + node['label']
        for child in node['children']:
            print_node(child, spaces+4)
    
    print_node(tree, 0)


def print_tree_structure_to_dot_file(tree, dot_filename):
    def get_name(index):
        return 'n%s' % index

    def create_node(index, label):
        label, _ = escape_encode(label.encode('utf-8'))
        return '\t{NAME} [label="{LABEL}"];\n'.format(NAME=get_name(index), LABEL=label)

    def create_connection(node_index, child_index):
        return '\t{NODE_NAME} -> {CHILD_NAME};\n'.format(NODE_NAME=get_name(node_index), 
                                                         CHILD_NAME=get_name(child_index))

    def print_node(node):
        out_file.write(create_node(node['index'], node['label']))

        for child in node['children']:
            print_node(child)
            out_file.write(create_connection(node['index'], child['index']))


    with open(dot_filename, 'w') as out_file:
        out_file.write('digraph lactose_program {\n')    

        print_node(tree)            

        out_file.write('}\n')


def print_tree_structure_to_pdf_file(tree, pdf_filename):
    _, tmp_dot_filename = tempfile.mkstemp(suffix='.dot')
    
    print_tree_structure_to_dot_file(tree, tmp_dot_filename)

    call(['dot', '-Tpdf', tmp_dot_filename, '-o', pdf_filename])