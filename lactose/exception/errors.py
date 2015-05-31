class LactoseError():
    def __init__(self, line, column, msg):
        self.line = line
        self.column = column
        self.msg = msg

    def __str__(self):
        return '[{LINE}, {COLUMN}]: {MSG}'.format(LINE=self.line, COLUMN=self.column, MSG=self.msg)


class LactoseSyntaxError(LactoseError):
    pass

class IdentifierNotFoundError(LactoseError):
    def __init__(self, node):
        self.line = node.antlr_node.symbol.line
        self.column = node.antlr_node.symbol.column
        self.msg = 'Identifier {IDENT} not found.'.format(IDENT=node.text)

class TooManySyntaxErrorException(Exception):
    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        return 'Too many syntax errors: {NUM_OF_ERRORS}'.format(NUM_OF_ERRORS=self.errors)