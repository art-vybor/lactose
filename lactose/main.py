import sys
import argparse
from subprocess import call

from lactose.compiler import get_lexems, get_ast_tree, get_token_name, compile_to_file


def replace_filename_extension(filepath, extension):
    return '{FILEPATH_CUTTED}.{EXTENTION}'.format(FILEPATH_CUTTED=filepath.rsplit('.', 1)[0], EXTENTION=extension)


def parse_args():
    parser = argparse.ArgumentParser(description='Lactose command line interface.')

    parser.add_argument('-i', metavar='filename', dest='input_file', required=True, help='input file')
    parser.add_argument('-o', metavar='filename', dest='output_file', required=False,
                        help='output file (default: input_file with rkt extension)')
    parser.add_argument('--run', action='store_true', help='execute output_file')
    parser.add_argument('--format', action='store_true', help='apply lisp formatter to output file')

    group = parser.add_argument_group('debug mode')
    group.add_argument('--stack_trace', action='store_true', help='enable stack trace printing')
    group.add_argument('--lexems', action='store_true', help='print lexems')
    group.add_argument('--console_tree', action='store_true', help='print ast tree to console')
    group.add_argument('--pdf_tree', action='store_true', help='print ast tree to pdf')
    
    args = parser.parse_args()

    if not args.output_file:
        args.output_file = replace_filename_extension(args.input_file, 'rkt')

    if args.format:
        print 'format functionality not released yet'

    return args


def main():
    sys.tracebacklimit = 0

    args = parse_args()
    if any([args.lexems, args.console_tree, args.pdf_tree, args.stack_trace]):
        print 'debug mode on'

    if args.stack_trace:
        sys.tracebacklimit = 1

    if args.lexems:
        lexems = get_lexems(args.input_file)
        for lexem in lexems:
            print '{LEXEM} {LEXEM_NAME}'.format(LEXEM=str(lexem),LEXEM_NAME=get_token_name(lexem))

    ast_tree = get_ast_tree(filepath=args.input_file)

    if args.console_tree:
        ast_tree.print_to_console()

    if args.pdf_tree:
        pdf_filename = replace_filename_extension(args.input_file, 'pdf')
        ast_tree.print_to_pdf_file(pdf_filename)
        print 'tree in pdf written at {FILENAME}'.format(FILENAME=pdf_filename)

    compile_to_file(ast_tree, args.output_file)
    print 'result written at {FILENAME}'.format(FILENAME=args.output_file)

    if args.run:    
        call(['racket', args.output_file])
