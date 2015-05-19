import argparse
import os
import tempfile

from antlr4 import *
from antlr4.tree import *

from lactose.grammar.lactoseLexer import lactoseLexer
from lactose.grammar.lactoseParser import lactoseParser
from lactose.ast import AST, ASTNode

def parse_args():
    parser = argparse.ArgumentParser(description='Lactose command line interface.')

    parser.add_argument('-i', help='name of input file',
        metavar='path', dest='input_path', required=True)
    parser.add_argument('-o', help='name of output file',
        metavar='path', dest='output_path', required=False)
    
    return parser.parse_args()

def get_lisp_tree(tree_structure):
    lisp_tree = []

    print tree_structure['label']
    if tree_structure['label'] == 'function_declare':
        func_elems = tree_structure['children']
        lisp_tree.append('define')
        sublist = []
        sublist.append(func_elems[0]['text'])
        sublist.extend([arg['text'] for arg in func_elems[1]['children']])
        lisp_tree.append(sublist)
        lisp_tree.append(get_lisp_tree(func_elems[2]))

    elif tree_structure['label'] == 'function_body':

        lisp_tree.append('cond')
        for _child in tree_structure['children']:
            if _child['label'] == 'function_branch':
                lisp_subtree = []
                lisp_subtree.append(get_lisp_tree(_child['children'][0]))
                lisp_subtree.append(_child['children'][2]['text'])
                lisp_tree.append(lisp_subtree)

    elif tree_structure['label'] == 'condition':
        print 1
        if tree_structure['children'][1]['type'] == 'EQUAL':
            lisp_tree.append('=')
        elif tree_structure['children'][1]['type'] == 'LESS':
            lisp_tree.append('<')
        elif tree_structure['children'][1]['type'] == 'MR':
            lisp_tree.append('>')
        lisp_tree.append(tree_structure['children'][0]['text'])
        lisp_tree.append(tree_structure['children'][2]['text'])



            #get_lisp_tree(child)

        #if 'text' in child:
            #print child['text']
    return lisp_tree

def print_lisp_tree(lisp_tree):
    print '(',
    for elem in lisp_tree:
        if isinstance(elem, list):
            print_lisp_tree(elem)
        else:
            print elem,
    print ')',


def main():
    args = parse_args()

    in_file = os.path.abspath(args.input_path)
    out_file = in_file.rsplit('.', 1)[0] + '.pdf'

    input = FileStream(in_file) #FileStream(args.input_path) 
    lexer = lactoseLexer(input)
    stream = CommonTokenStream(lexer)
    parser = lactoseParser(stream)
    tree = parser.lactose_program()
    
    ast_tree = AST(tree)

    #lisp_tree = get_lisp_tree(tree_structure['children'][0])

    #print_lisp_tree(lisp_tree)

    ast_tree.print_to_console()

    ast_tree.print_to_pdf_file(out_file)