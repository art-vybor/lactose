
class ASTNode:
    def __init__(self, index):
        self.index = index
        self.text = ''
        self.name = ''
        self.terminal = False
        self.children = []
        self.antlr_node = None

        self.parent = None

        self.symbol_table = {}
        self.symbol = None #(symbol, args)

    def __str__(self):
        if self.terminal:
            return "{TYPE} '{TEXT}'".format(TYPE=self.name, TEXT=self.text,)
        else:
            return "{NAME}{SYMBOL}{TABLE}".format(NAME=self.name, 
                                                    SYMBOL=self.get_symbol_in_str() if self.symbol else '',
                                                    TABLE=' | table:' + str(self.symbol_table) if self.symbol_table else '')

    def get_symbol_in_str(self):
        return ' {NAME}({ARGS})'.format(NAME=self.symbol[0], ARGS=', '.join(self.symbol[1]))

    def add_symbol_to_table(self, symbol):
        name, args = symbol
        self.symbol_table[name]=args

    def add_child(self, child):
        self.children.append(child)