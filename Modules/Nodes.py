class Node:
    pass


class Program(Node):
    def __init__(self, nodes):
        self.nodes = nodes


class Decl(Node):
    def __init__(self, type_, id_):
        self.type_ = type_
        self.id_ = id_


class LowestIndex(Node):
    def __init__(self, lowestIndex):
        self.lowestIndex = lowestIndex


class HighestIndex(Node):
    def __init__(self, highestIndex):
        self.highestIndex = highestIndex


class ArrayDecl(Node):
    def __init__(self, type_, id_, lowestIndex, highestIndex, elems):
        self.type_ = type_
        self.id_ = id_
        self.lowestIndex = lowestIndex
        self.highestIndex = highestIndex
        self.elems = elems


class StringDecl(Node):
    def __init__(self, id_, length):
        self.id_ = id_
        self.length = length


class ArrayElem(Node):
    def __init__(self, id_, index):
        self.id_ = id_
        self.index = index


class Assign(Node):
    def __init__(self, id_, expr):
        self.id_ = id_
        self.expr = expr


class If(Node):
    def __init__(self, cond, true, false):
        self.cond = cond
        self.true = true
        self.false = false


class While(Node):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block


class For(Node):
    def __init__(self, init, finishNumber, block):
        self.init = init
        self.finishNumber = finishNumber
        self.block = block


class Repeat(Node):
    def __init__(self, block, cond):
        self.block = block
        self.cond = cond


class FuncImpl(Node):
    def __init__(self, type_, id_, params, block, var):
        self.type_ = type_
        self.id_ = id_
        self.params = params
        self.block = block
        self.var = var


class ProcImpl(Node):
    def __init__(self, id_, params, block, var):
        self.id_ = id_
        self.params = params
        self.block = block
        self.var = var


class VarDeclaration(Node):
    def __init__(self, declarations):
        self.declarations = declarations


class FuncCall(Node):
    def __init__(self, id_, args):
        self.id_ = id_
        self.args = args


class Block(Node):
    def __init__(self, nodes):
        self.nodes = nodes


class Params(Node):
    def __init__(self, params):
        self.params = params


class Args(Node):
    def __init__(self, args):
        self.args = args


class Elems(Node):
    def __init__(self, elems):
        self.elems = elems


class Break(Node):
    pass


class Continue(Node):
    pass


class Exit(Node):
    def __init__(self, args):
        self.args = args


class Type(Node):
    def __init__(self, value):
        self.value = value


class Int(Node):
    def __init__(self, value):
        self.value = value


class Char(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value


class Boolean(Node):
    def __init__(self, value):
        self.value = value


class Id(Node):
    def __init__(self, value):
        self.value = value


class Real(Node):
    def __init__(self, value):
        self.value = value


class BinOp(Node):
    def __init__(self, symbol, first, second):
        self.symbol = symbol
        self.first = first
        self.second = second


class UnOp(Node):
    def __init__(self, symbol, first):
        self.symbol = symbol
        self.first = first


class FormatedNumber(Node):
    def __init__(self, exp, beforeComma, afterComma):
        self.exp = exp
        self.beforeComma = beforeComma
        self.afterComma = afterComma
