import sys

sys.tracebacklimit = 0

class Error(Exception):
    pass

class LactoseSyntaxError(Error):
    def __init__(self, line, column, msg):
        self.line = line
        self.column = column
        self.msg = msg

    def __str__(self):
        return '[{LINE}, {COLUMN}]: {MSG}'.format(LINE=self.line, COLUMN=self.column, MSG=self.msg)
