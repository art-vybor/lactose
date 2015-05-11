# Generated from java-escape by ANTLR 4.5
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO


def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\2")
        buf.write(u"\7$\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\3")
        buf.write(u"\2\3\2\3\2\3\2\3\2\3\2\3\3\3\3\3\4\3\4\3\5\6\5\32\n\5")
        buf.write(u"\r\5\16\5\33\3\6\6\6\37\n\6\r\6\16\6 \3\6\3\6\2\2\7\3")
        buf.write(u"\3\5\4\7\5\t\6\13\7\3\2\4\3\2c|\5\2\13\f\17\17\"\"%\2")
        buf.write(u"\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3")
        buf.write(u"\2\2\2\3\r\3\2\2\2\5\24\3\2\2\2\7\26\3\2\2\2\t\31\3\2")
        buf.write(u"\2\2\13\36\3\2\2\2\r\16\7j\2\2\16\17\7g\2\2\17\20\7n")
        buf.write(u"\2\2\20\21\7n\2\2\21\22\7q\2\2\22\23\7y\2\2\23\4\3\2")
        buf.write(u"\2\2\24\25\7G\2\2\25\6\3\2\2\2\26\27\7S\2\2\27\b\3\2")
        buf.write(u"\2\2\30\32\t\2\2\2\31\30\3\2\2\2\32\33\3\2\2\2\33\31")
        buf.write(u"\3\2\2\2\33\34\3\2\2\2\34\n\3\2\2\2\35\37\t\3\2\2\36")
        buf.write(u"\35\3\2\2\2\37 \3\2\2\2 \36\3\2\2\2 !\3\2\2\2!\"\3\2")
        buf.write(u"\2\2\"#\b\6\2\2#\f\3\2\2\2\5\2\33 \3\b\2\2")
        return buf.getvalue()


class lactoseLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]


    T__0 = 1
    E = 2
    Q = 3
    ID = 4
    WS = 5

    modeNames = [ u"DEFAULT_MODE" ]

    literalNames = [ u"<INVALID>",
            u"'hellow'", u"'E'", u"'Q'" ]

    symbolicNames = [ u"<INVALID>",
            u"E", u"Q", u"ID", u"WS" ]

    ruleNames = [ u"T__0", u"E", u"Q", u"ID", u"WS" ]

    grammarFileName = u"lactose.g4"

    def __init__(self, input=None):
        super(lactoseLexer, self).__init__(input)
        self.checkVersion("4.5")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


