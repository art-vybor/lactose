import argparse

from antlr4 import *
from antlr4.tree import *

from lactose.grammar.lactoseLexer import lactoseLexer
from lactose.grammar.lactoseParser import lactoseParser

def parse_args():
    parser = argparse.ArgumentParser(description='Lactose command line interface.')

    parser.add_argument('-i', help='name of input file',
        metavar='path', dest='input_path', required=True)
    parser.add_argument('-o', help='name of output file',
        metavar='path', dest='output_path', required=False)
    
    return parser.parse_args()

def print_level_order(tree, indent):
    print '{0}{1}'.format('   '*indent, tree.text)
    for child in tree.getChildren():
        print_level_order(child, indent+1)

def dfs_print(tree, spaces=0):
    for child in tree.children:
        if 'symbol' in child.__dict__:
            print ' '*spaces + str(child)
        else:
            dfs_print(child, spaces+4)

def main():
    args = parse_args()

    input = FileStream(args.input_path)
    lexer = lactoseLexer(input)
    stream = CommonTokenStream(lexer)
    parser = lactoseParser(stream)
    t = parser.r()
    dfs_print(t)