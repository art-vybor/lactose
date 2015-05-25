class LactoseSyntaxError():
    def __init__(self, line, column, msg):
        self.line = line
        self.column = column
        self.msg = msg

    def __str__(self):
        return '[{LINE}, {COLUMN}]: {MSG}'.format(LINE=self.line, COLUMN=self.column, MSG=self.msg)


class TooManySyntaxErrorException(Exception):
    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        return 'Too many syntax errors: {NUM_OF_ERRORS}'.format(NUM_OF_ERRORS=self.errors)