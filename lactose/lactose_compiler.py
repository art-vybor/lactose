from antlr4 import FileStream, CommonTokenStream

from lactose.ast import AST
from lactose.lisp_tree import LispTree
from lactose.grammar.lactoseLexer import lactoseLexer
from lactose.grammar.lactoseParser import lactoseParser
from lactose.exception.error_listener import AntlrErrorListener

def get_lexer(filepath):
    file_stream = FileStream(filepath)
    return lactoseLexer(file_stream)

def get_lexems(filepath):
    lexer = get_lexer(filepath)
    return lexer.getAllTokens()

def get_ast_tree(filepath):
    lexer = get_lexer(filepath)
    stream = CommonTokenStream(lexer)

    parser = lactoseParser(stream)
    parser._listeners=[AntlrErrorListener.INSTANCE]
        
    tree = parser.lactose_program()
    return AST(tree)

def compile_to_file(ast_tree, filepath):
    tree = LispTree(ast_tree)
    with open(filepath, 'w') as f:
        f.write('#lang r5rs\n')
        f.write(str(tree))

def get_token_name(token):
    return lactoseParser.symbolicNames[token.type]