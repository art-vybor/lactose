from antlr4 import FileStream, CommonTokenStream
from antlr4.InputStream import InputStream

from lactose.ast.tree import AST
from lactose.lisp_tree import LispTree
from lactose.exception.errors import TooManySyntaxErrorException, TooManySemanticErrorException
from lactose.grammar.lactoseLexer import lactoseLexer
from lactose.grammar.lactoseParser import lactoseParser
from lactose.exception.error_listener import set_error_listener, get_error_listener


def get_lexer(StreamClass, data):
    file_stream = StreamClass(data)
    lexer = lactoseLexer(file_stream)
    set_error_listener(lexer)
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
    set_error_listener(parser)
    tree = parser.parse()
    if get_error_listener().errors:
        raise TooManySyntaxErrorException(get_error_listener().errors)
        
    return AST(tree)


def compile_to_string(ast_tree):
    tree = LispTree(ast_tree)
    if tree.errors:
        raise TooManySemanticErrorException(tree.errors)
    return '#lang r5rs\n' + str(tree)


def compile_to_file(ast_tree, filepath):
    with open(filepath, 'w') as f:
        f.write(compile_to_string(ast_tree))


def get_token_name(token):
    return lactoseParser.symbolicNames[token.type]