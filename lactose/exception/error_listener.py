from antlr4.error.ErrorListener import ConsoleErrorListener

from lactose.exception.errors import LactoseSyntaxError


class AntlrErrorListener(ConsoleErrorListener):
    INSTANCE = None
    errors = 0

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors += 1
        print LactoseSyntaxError(line, column, msg)


def reset_error_listener(listener=AntlrErrorListener):
    listener.INSTANCE = None


def set_error_listener(obj, listener=AntlrErrorListener):
    if not listener.INSTANCE:
        listener.INSTANCE = listener() 
    obj._listeners = [listener.INSTANCE]


def get_error_listener(listener=AntlrErrorListener):
    return listener.INSTANCE