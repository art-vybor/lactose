from antlr4 import FileStream, CommonTokenStream, InputStream

from lactose.ast import AST
from lactose.lisp_tree import LispTree
from lactose.grammar.lactoseLexer import lactoseLexer
from lactose.grammar.lactoseParser import lactoseParser
from lactose.exception.error_listener import AntlrErrorListener

def get_lexer_from_string(string):
    stream = InputStream.InputStream(string)
    return lactoseLexer(stream)

def get_lexer_from_file(filepath):
    file_stream = FileStream(filepath)
    return lactoseLexer(file_stream)

def get_lexems(filepath):
    lexer = get_lexer_from_file(filepath)
    return lexer.getAllTokens()

def get_ast_tree(filepath=None, string=None):
    lexer = get_lexer_from_file(filepath) if filepath else get_lexer_from_string(string)
    stream = CommonTokenStream(lexer)

    parser = lactoseParser(stream)
    parser._listeners=[AntlrErrorListener.INSTANCE]
        
    tree = parser.lactose_program()
    return AST(tree)

def compile_to_string(ast_tree):
    tree = LispTree(ast_tree)
    return '#lang r5rs\n' + str(tree)

def compile_to_file(ast_tree, filepath):
    with open(filepath, 'w') as f:
        f.write(compile_to_string(ast_tree))

def get_token_name(token):
    return lactoseParser.symbolicNames[token.type]