# Generated from java-escape by ANTLR 4.5
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO
package = globals().get("__package__", None)
ischild = len(package)>0 if package is not None else False
if ischild:
    from .HelloListener import HelloListener
else:
    from HelloListener import HelloListener
def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3")
        buf.write(u"\7\23\4\2\t\2\4\3\t\3\4\4\t\4\3\2\3\2\3\2\3\3\3\3\3\3")
        buf.write(u"\3\3\3\4\3\4\3\4\3\4\2\2\5\2\4\6\2\2\17\2\b\3\2\2\2\4")
        buf.write(u"\13\3\2\2\2\6\17\3\2\2\2\b\t\7\3\2\2\t\n\5\4\3\2\n\3")
        buf.write(u"\3\2\2\2\13\f\7\6\2\2\f\r\7\4\2\2\r\16\5\6\4\2\16\5\3")
        buf.write(u"\2\2\2\17\20\7\6\2\2\20\21\7\5\2\2\21\7\3\2\2\2\2")
        return buf.getvalue()


class HelloParser ( Parser ):

    grammarFileName = "java-escape"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"'hellow'", u"'E'", u"'Q'" ]

    symbolicNames = [ u"<INVALID>", u"<INVALID>", u"E", u"Q", u"ID", u"WS" ]

    RULE_r = 0
    RULE_t = 1
    RULE_q = 2

    ruleNames =  [ u"r", u"t", u"q" ]

    EOF = Token.EOF
    T__0=1
    E=2
    Q=3
    ID=4
    WS=5

    def __init__(self, input):
        super(HelloParser, self).__init__(input)
        self.checkVersion("4.5")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class RContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(HelloParser.RContext, self).__init__(parent, invokingState)
            self.parser = parser

        def t(self):
            return self.getTypedRuleContext(HelloParser.TContext,0)


        def getRuleIndex(self):
            return HelloParser.RULE_r

        def enterRule(self, listener):
            if isinstance( listener, HelloListener ):
                listener.enterR(self)

        def exitRule(self, listener):
            if isinstance( listener, HelloListener ):
                listener.exitR(self)




    def r(self):

        localctx = HelloParser.RContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_r)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 6
            self.match(HelloParser.T__0)
            self.state = 7
            self.t()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(HelloParser.TContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(HelloParser.ID, 0)

        def E(self):
            return self.getToken(HelloParser.E, 0)

        def q(self):
            return self.getTypedRuleContext(HelloParser.QContext,0)


        def getRuleIndex(self):
            return HelloParser.RULE_t

        def enterRule(self, listener):
            if isinstance( listener, HelloListener ):
                listener.enterT(self)

        def exitRule(self, listener):
            if isinstance( listener, HelloListener ):
                listener.exitT(self)




    def t(self):

        localctx = HelloParser.TContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_t)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 9
            self.match(HelloParser.ID)
            self.state = 10
            self.match(HelloParser.E)
            self.state = 11
            self.q()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class QContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(HelloParser.QContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(HelloParser.ID, 0)

        def Q(self):
            return self.getToken(HelloParser.Q, 0)

        def getRuleIndex(self):
            return HelloParser.RULE_q

        def enterRule(self, listener):
            if isinstance( listener, HelloListener ):
                listener.enterQ(self)

        def exitRule(self, listener):
            if isinstance( listener, HelloListener ):
                listener.exitQ(self)




    def q(self):

        localctx = HelloParser.QContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_q)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13
            self.match(HelloParser.ID)
            self.state = 14
            self.match(HelloParser.Q)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx




