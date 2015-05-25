from antlr4 import FileStream, CommonTokenStream
from antlr4.InputStream import InputStream

from lactose.ast import AST
from lactose.lisp_tree import LispTree
from lactose.exception.errors import TooManySyntaxErrorException
from lactose.grammar.lactoseLexer import lactoseLexer
from lactose.grammar.lactoseParser import lactoseParser
from lactose.exception.error_listener import AntlrErrorListener


def get_lexer(StreamClass, data):
    file_stream = StreamClass(data)
    lexer = lactoseLexer(file_stream) 
    lexer._listeners=[AntlrErrorListener.INSTANCE]
    return lexer

def get_lexer_from_string(string):
    return get_lexer(InputStream, string)


def get_lexer_from_file(filepath):
    return get_lexer(FileStream, filepath)


def get_lexems(filepath):
    lexer = get_lexer_from_file(filepath)
    return lexer.getAllTokens()


def get_ast_tree(filepath=None, string=None):
    lexer = get_lexer_from_file(filepath) if filepath else get_lexer_from_string(string)
    stream = CommonTokenStream(lexer)

    parser = lactoseParser(stream)
    parser._listeners=[AntlrErrorListener.INSTANCE]
    tree = parser.lactose_program()

    if AntlrErrorListener.INSTANCE.errors:
        raise TooManySyntaxErrorException(AntlrErrorListener.INSTANCE.errors)
        
    return AST(tree)


def compile_to_string(ast_tree):
    tree = LispTree(ast_tree)
    return '#lang r5rs\n' + str(tree)


def compile_to_file(ast_tree, filepath):
    with open(filepath, 'w') as f:
        f.write(compile_to_string(ast_tree))


def get_token_name(token):
    return lactoseParser.symbolicNames[token.type]