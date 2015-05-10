from antlr4 import *
from antlr4.tree import *
from HelloLexer import HelloLexer
from HelloParser import HelloParser
from HelloListener import HelloListener
import sys

class KeyPrinter(HelloListener):
    def enterR(self, ctx):
        print(ctx.getText()) 

    def exitR(self, ctx):         
        print(ctx.getText()) 

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


def main(argv):
    input = FileStream(argv[1])
    lexer = HelloLexer(input)
    stream = CommonTokenStream(lexer)
    parser = HelloParser(stream)
    t = parser.r()
    dfs_print(t)
    # print(type(t))
    #tree = parser.r()
    #toStringTree(t, parser)
    #print(tree.toStringTree())
    #print_level_order(t, 0)
    
    #printer = KeyPrinter()
    #walker = ParseTreeWalker()
    #walker.walk(printer, t)