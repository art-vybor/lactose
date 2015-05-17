import argparse

from antlr4 import *
from antlr4.tree import *

from lactose.grammar.lactoseLexer import lactoseLexer
from lactose.grammar.lactoseParser import lactoseParser
from lactose.printer import get_tree_structure, print_tree_structure_to_console, print_tree_structure_to_dot_file, print_tree_structure_to_pdf_file

def parse_args():
    parser = argparse.ArgumentParser(description='Lactose command line interface.')

    parser.add_argument('-i', help='name of input file',
        metavar='path', dest='input_path', required=True)
    parser.add_argument('-o', help='name of output file',
        metavar='path', dest='output_path', required=False)
    
    return parser.parse_args()

def main():
    args = parse_args()

    in_file = '/home/avybornov/git/lactose/sample.lc'
    out_file = '/home/avybornov/git/lactose/sample.pdf'

    input = FileStream(in_file) #FileStream(args.input_path)
    lexer = lactoseLexer(input)
    stream = CommonTokenStream(lexer)
    parser = lactoseParser(stream)
    tree = parser.lactose_program()
    #for child in tree.children:
    tree_structure = get_tree_structure(tree)

    print_tree_structure_to_pdf_file(tree_structure, out_file)
