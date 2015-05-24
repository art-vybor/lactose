#from __future__ import print_function
import argparse
import os
import tempfile


from antlr4.error.ErrorListener import ConsoleErrorListener
from antlr4 import *
from antlr4.tree import *

from lactose.grammar.lactoseLexer import lactoseLexer
from lactose.grammar.lactoseParser import lactoseParser
from lactose.ast import AST
from lactose.lisp_tree import LispTree
from lactose.exception import LactoseSyntaxError

class AdvancedErrorListener(ConsoleErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise LactoseSyntaxError(line, column, msg)

AdvancedErrorListener.INSTANCE = AdvancedErrorListener()

def parse_args():
    parser = argparse.ArgumentParser(description='Lactose command line interface.')

    parser.add_argument('-i', help='name of input file',
        metavar='path', dest='input_path', required=True)
    parser.add_argument('-o', help='name of output file',
        metavar='path', dest='output_path', required=False)
    
    return parser.parse_args()

def main():
    #raise SyntaxError('asdasddas')
    args = parse_args()

    in_file = os.path.abspath(args.input_path)
    out_file = in_file.rsplit('.', 1)[0] + '.pdf'
    out_lisp_file = in_file.rsplit('.', 1)[0] + '.rkt'

    # input = FileStream(in_file)

    # lexer = lactoseLexer(input)
    # for x in map(lambda x: '%s %s' % (str(x), lactoseParser.symbolicNames[x.type]), lexer.getAllTokens()):
    #     print x
    input = FileStream(in_file)

    lexer = lactoseLexer(input)
    
    stream = CommonTokenStream(lexer)
    

    parser = lactoseParser(stream)
    parser._listeners=[AdvancedErrorListener.INSTANCE]
        
    tree = parser.lactose_program()
    #print 'errors: ', parser._syntaxErrors
    #print 2
    ast_tree = AST(tree)

    #print ast_tree.root.children

    
    #ast_tree.print_to_console()

    #ast_tree.print_to_pdf_file(out_file)

    tree = LispTree(ast_tree)
    #print tree.tree

    with open(out_lisp_file, 'w') as f:
        f.write('#lang r5rs\n')
        f.write(str(tree))
        f.write('(newline)')

    from subprocess import call
    #call(['racket', out_lisp_file])


    #print tree