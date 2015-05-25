from antlr4.error.ErrorListener import ConsoleErrorListener
from lactose.exception.errors import LactoseSyntaxError


class AntlrErrorListener(ConsoleErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise LactoseSyntaxError(line, column, msg)

AntlrErrorListener.INSTANCE = AntlrErrorListener()