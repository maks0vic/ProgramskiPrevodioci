from functools import wraps
import pickle
from Modules.ClassEnum import Class
from Modules.Nodes import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr = tokens.pop(0)
        self.prev = None

    def restorable(call):
        @wraps(call)
        def wrapper(self, *args, **kwargs):
            state = pickle.dumps(self.__dict__)
            result = call(self, *args, **kwargs)
            self.__dict__ = pickle.loads(state)
            return result

        return wrapper

    def eat(self, class_):
        if self.curr.class_ == class_:
            self.prev = self.curr
            self.curr = self.tokens.pop(0)
        else:
            self.die_type(class_.name, self.curr.class_.name)

    def program(self):
        nodes = []
        while self.curr.class_ != Class.EOF:
            if self.curr.class_ == Class.BEGIN:
                self.eat(Class.BEGIN)
                nodes.append(self.block())
            elif self.curr.class_ == Class.PROCEDURE:
                nodes.append(self.decl())
            elif self.curr.class_ == Class.FUNCTION:
                nodes.append(self.decl())
            elif self.curr.class_ == Class.VAR:
                declList = self.decl()
                nodes.append(VarDeclaration(declList))
            else:
                self.die_deriv(self.program.__name__)
        return Program(nodes)

    def id_(self):
        id_ = Id(self.curr.lexeme)
        self.eat(Class.ID)
        if self.curr.class_ == Class.LPAREN and self.is_func_call():
            self.eat(Class.LPAREN)
            args = self.args()
            self.eat(Class.RPAREN)
            return FuncCall(id_, args)
        elif self.curr.class_ == Class.LBRACKET:
            self.eat(Class.LBRACKET)
            index = self.expr()
            self.eat(Class.RBRACKET)
            id_ = ArrayElem(id_, index)
        if self.curr.class_ == Class.ASSIGN:
            self.eat(Class.ASSIGN)
            expr = self.expr()
            return Assign(id_, expr)
        else:
            return id_

    def decl(self):
        if self.curr.class_ == Class.PROCEDURE:
            self.eat(Class.PROCEDURE)
            id_ = self.id_()
            self.eat(Class.LPAREN)
            params = self.params()
            self.eat(Class.RPAREN)
            self.eat(Class.SEMICOLON)
            var = None
            if self.curr.class_ == Class.VAR:
                var = self.decl()
            self.eat(Class.BEGIN)
            block = self.block()
            self.eat(Class.SEMICOLON)
            if var is None:
                return ProcImpl(id_, params, block, None)
            else:
                return ProcImpl(id_, params, block, VarDeclaration(var))
        elif self.curr.class_ == Class.FUNCTION:
            self.eat(Class.FUNCTION)
            id_ = self.id_()
            self.eat(Class.LPAREN)
            params = self.params()
            self.eat(Class.RPAREN)
            self.eat(Class.COLON)
            type_ = self.type_()
            self.eat(Class.SEMICOLON)
            var = None
            if self.curr.class_ == Class.VAR:
                var = self.decl()
            self.eat(Class.BEGIN)
            block = self.block()
            self.eat(Class.SEMICOLON)
            if var is None:
                return FuncImpl(type_, id_, params, block, None)
            else:
                return FuncImpl(type_, id_, params, block, VarDeclaration(var))
        elif self.curr.class_ == Class.VAR:
            declarations = []
            self.eat(Class.VAR)
            while self.curr.class_ != Class.BEGIN and self.curr.class_ != Class.PROCEDURE and self.curr.class_ != Class.FUNCTION:
                idList = []
                while self.curr.class_ != Class.COLON:
                    id_ = self.id_()
                    idList.append(id_)
                    if self.curr.class_ != Class.COLON:
                        self.eat(Class.COMMA)
                self.eat(Class.COLON)
                if self.curr.class_ != Class.ARRAY:
                    type_ = self.type_()
                    if type_.value == 'string' and self.curr.class_ == Class.LBRACKET:
                        self.eat(Class.LBRACKET)
                        length = self.expr()
                        self.eat(Class.RBRACKET)
                        for i in idList:
                            declarations.append(StringDecl(i, length))
                    else:
                        for i in idList:
                            if type_.value == 'string':
                                declarations.append(StringDecl(i, None))
                            else:
                                declarations.append(Decl(type_, i))
                else:
                    elems = None
                    self.eat(Class.ARRAY)
                    self.eat(Class.LBRACKET)
                    lowestIndex = self.expr()
                    self.eat(Class.DOT)
                    self.eat(Class.DOT)
                    highestIndex = self.expr()
                    self.eat(Class.RBRACKET)
                    self.eat(Class.OF)
                    type_ = self.type_()
                    if self.curr.class_ != Class.SEMICOLON:
                        self.eat(Class.EQ)
                        self.eat(Class.LPAREN)
                        elems = self.elems()
                        self.eat(Class.RPAREN)
                    for i in idList:
                        declarations.append(
                            ArrayDecl(type_, id_, LowestIndex(lowestIndex), HighestIndex(highestIndex), elems))
                self.eat(Class.SEMICOLON)
            return declarations

    def if_(self):
        self.eat(Class.IF)
        cond = self.logic()
        self.eat(Class.THEN)
        self.eat(Class.BEGIN)
        true = self.block()
        false = None
        if self.curr.class_ == Class.ELSE:
            self.eat(Class.ELSE)
            if self.curr.class_ == Class.IF:
                false = self.if_()
            else:
                self.eat(Class.BEGIN)
                false = self.block()
                self.eat(Class.SEMICOLON)
        else:
            self.eat(Class.SEMICOLON)
        return If(cond, true, false)

    def while_(self):
        self.eat(Class.WHILE)
        cond = self.logic()
        self.eat(Class.DO)
        self.eat(Class.BEGIN)
        block = self.block()
        self.eat(Class.SEMICOLON)
        return While(cond, block)

    def for_(self):
        self.eat(Class.FOR)
        init = self.id_()
        if self.curr.class_ == Class.TO:
            self.eat(Class.TO)
        else:
            self.eat(Class.DOWNTO)
        finishNumber = self.expr()
        self.eat(Class.DO)
        self.eat(Class.BEGIN)
        block = self.block()
        self.eat(Class.SEMICOLON)
        return For(init, finishNumber, block)

    def repeatBlock(self):
        nodes = []
        if self.curr.class_ in [Class.REPEAT, Class.IF, Class.WHILE, Class.FOR, Class.BREAK, Class.CONTINUE, Class.TYPE,
                                Class.ID, Class.EXIT]:
            while self.curr.class_ != Class.UNTIL:
                if self.curr.class_ == Class.IF:
                    nodes.append(self.if_())
                elif self.curr.class_ == Class.WHILE:
                    nodes.append(self.while_())
                elif self.curr.class_ == Class.FOR:
                    nodes.append(self.for_())
                elif self.curr.class_ == Class.BREAK:
                    nodes.append(self.break_())
                elif self.curr.class_ == Class.CONTINUE:
                    nodes.append(self.continue_())
                elif self.curr.class_ == Class.TYPE:
                    nodes.append(self.decl())
                elif self.curr.class_ == Class.REPEAT:
                    nodes.append(self.repeat_())
                elif self.curr.class_ == Class.ID:
                    nodes.append(self.id_())
                    self.eat(Class.SEMICOLON)
                elif self.curr.class_ == Class.EXIT:
                    nodes.append(self.exit_())
                else:
                    self.die_deriv(self.block.__name__)

        return Block(nodes)

    def repeat_(self):
        self.eat(Class.REPEAT)
        block = self.repeatBlock()
        self.eat(Class.UNTIL)
        cond = self.logic()#false samo
        self.eat(Class.SEMICOLON)
        return Repeat(block, cond)

    @restorable
    def is_eof(self):
        try:
            self.eat(Class.DOT)
            if self.curr.class_ == Class.EOF:
                return True
            return False
        except:
            return False

    def block(self):
        nodes = []
        if self.curr.class_ in [Class.REPEAT, Class.IF, Class.WHILE, Class.FOR, Class.BREAK, Class.CONTINUE, Class.TYPE,
                                Class.ID, Class.EXIT]:
            while self.curr.class_ != Class.END:
                if self.curr.class_ == Class.IF:
                    nodes.append(self.if_())
                elif self.curr.class_ == Class.WHILE:
                    nodes.append(self.while_())
                elif self.curr.class_ == Class.FOR:
                    nodes.append(self.for_())
                elif self.curr.class_ == Class.BREAK:
                    nodes.append(self.break_())
                elif self.curr.class_ == Class.CONTINUE:
                    nodes.append(self.continue_())
                elif self.curr.class_ == Class.TYPE:
                    nodes.append(self.decl())
                elif self.curr.class_ == Class.REPEAT:
                    nodes.append(self.repeat_())
                elif self.curr.class_ == Class.ID:
                    nodes.append(self.id_())
                    self.eat(Class.SEMICOLON)
                elif self.curr.class_ == Class.EXIT:
                    nodes.append(self.exit_())
                else:
                    self.die_deriv(self.block.__name__)
            self.eat(Class.END)
            if self.curr.class_ == Class.DOT and self.is_eof():
                self.eat(Class.DOT)

        return Block(nodes)

    def params(self):
        params = []
        idList = []
        isFirst = True

        while self.curr.class_ != Class.RPAREN:
            if not isFirst:
                self.eat(Class.SEMICOLON)
            isFirst = False
            while self.curr.class_ != Class.COLON:
                id_ = self.id_()
                idList.append(id_)
                if self.curr.class_ != Class.COLON:
                    self.eat(Class.COMMA)

            self.eat(Class.COLON)
            type_ = self.type_()
            for i in idList:
                params.append(Decl(type_, i))
            idList.clear()
        return Params(params)

    def args(self):
        args = []
        while self.curr.class_ != Class.RPAREN:
            if len(args) > 0:
                self.eat(Class.COMMA)
            args.append(self.expr())
        return Args(args)

    def elems(self):
        elems = []
        while self.curr.class_ != Class.RPAREN:
            if len(elems) > 0:
                self.eat(Class.COMMA)
            elems.append(self.expr())
        return Elems(elems)

    def exit_(self):
        self.eat(Class.EXIT)
        args = None
        if self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            args = self.args()
            self.eat(Class.RPAREN)
            self.eat(Class.SEMICOLON)
            return Exit(args)
        self.eat(Class.SEMICOLON)
        return Exit(args)

    def break_(self):
        self.eat(Class.BREAK)
        self.eat(Class.SEMICOLON)
        return Break()

    def continue_(self):
        self.eat(Class.CONTINUE)
        self.eat(Class.SEMICOLON)
        return Continue()

    def type_(self):
        type_ = Type(self.curr.lexeme)
        self.eat(Class.TYPE)
        return type_

    def factor(self):
        if self.curr.class_ == Class.INT:
            value = Int(self.curr.lexeme)
            self.eat(Class.INT)
            return value
        elif self.curr.class_ == Class.CHAR:
            value = Char(self.curr.lexeme)
            self.eat(Class.CHAR)
            return value
        elif self.curr.class_ == Class.STRING:
            value = String(self.curr.lexeme)
            self.eat(Class.STRING)
            return value
        elif self.curr.class_ == Class.REAL:
            value = Real(self.curr.lexeme)
            self.eat(Class.REAL)
            return value
        elif self.curr.class_ == Class.BOOLEAN:
            value = Boolean(self.curr.lexeme)
            self.eat(Class.BOOLEAN)
            return value
        elif self.curr.class_ == Class.ID:
            first = self.id_()
            if self.curr.class_ in [Class.EQ, Class.NEQ, Class.LT, Class.GT, Class.LTE, Class.GTE]:
                op = self.curr.lexeme
                self.eat(self.curr.class_)
                second = self.expr()
                first = BinOp(op, first, second)
            return first
        elif self.curr.class_ in [Class.MINUS, Class.NOT]:
            op = self.curr
            self.eat(self.curr.class_)
            if self.curr.class_ == Class.LPAREN:
                self.eat(Class.LPAREN)
                first = self.logic()
                self.eat(Class.RPAREN)
            else:
                first = self.factor()
            return UnOp(op.lexeme, first)
        elif self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            first = self.logic()
            self.eat(Class.RPAREN)
            return first
        elif self.curr.class_ == Class.SEMICOLON:
            return None
        else:
            self.die_deriv(self.factor.__name__)

    def term(self):
        first = self.factor()
        while self.curr.class_ in [Class.STAR, Class.DIV, Class.MOD, Class.FWDSLASH, Class.EQ]:
            if self.curr.class_ == Class.STAR:
                op = self.curr.lexeme
                self.eat(Class.STAR)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.DIV:
                op = self.curr.lexeme
                self.eat(Class.DIV)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.MOD:
                op = self.curr.lexeme
                self.eat(Class.MOD)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.FWDSLASH:
                op = self.curr.lexeme
                self.eat(Class.FWDSLASH)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.EQ:
                op = self.curr.lexeme
                self.eat(Class.EQ)
                second = self.factor()
                first = BinOp(op, first, second)

        return first

    def expr(self):
        if self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            first = self.expr()
            self.eat(Class.RPAREN)
        else:
            first = self.term()
        if self.curr.class_ == Class.COLON:
            self.eat(Class.COLON)
            bfr = Int(self.curr.lexeme)
            self.eat(Class.INT)
            self.eat(Class.COLON)
            afr = Int(self.curr.lexeme)
            self.eat(Class.INT)
            first = FormatedNumber(first, bfr, afr)
        if self.curr.class_ in [Class.STAR, Class.DIV, Class.MOD, Class.FWDSLASH, Class.EQ]:
            op = self.curr.lexeme
            self.eat(self.curr.class_)
            second = self.term()
            first = BinOp(op, first, second)
        while self.curr.class_ in [Class.PLUS, Class.MINUS]:
            if self.curr.class_ == Class.PLUS:
                op = self.curr.lexeme
                self.eat(Class.PLUS)
                second = self.term()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.MINUS:
                op = self.curr.lexeme
                self.eat(Class.MINUS)
                second = self.term()
                first = BinOp(op, first, second)
        return first

    def compare(self):
        first = self.expr()
        if self.curr.class_ == Class.EQ:
            op = self.curr.lexeme
            self.eat(Class.EQ)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.NEQ:
            op = self.curr.lexeme
            self.eat(Class.NEQ)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.LT:
            op = self.curr.lexeme
            self.eat(Class.LT)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.GT:
            op = self.curr.lexeme
            self.eat(Class.GT)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.LTE:
            op = self.curr.lexeme
            self.eat(Class.LTE)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.GTE:
            op = self.curr.lexeme
            self.eat(Class.GTE)
            second = self.expr()
            return BinOp(op, first, second)
        else:
            return first

    def logic_term(self):
        first = self.compare()
        while self.curr.class_ == Class.AND:
            op = self.curr.lexeme
            self.eat(Class.AND)
            second = self.compare()
            first = BinOp(op, first, second)
        return first

    def logic(self):
        first = self.logic_term()
        while self.curr.class_ == Class.OR or self.curr.class_ == Class.XOR:
            if self.curr.class_ == Class.OR:
                op = self.curr.lexeme
                self.eat(Class.OR)
                second = self.logic_term()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.XOR:
                op = self.curr.lexeme
                self.eat(Class.XOR)
                second = self.logic_term()
                first = BinOp(op, first, second)

        return first

    @restorable
    def is_func_call(self):
        try:
            self.eat(Class.LPAREN)
            self.args()
            self.eat(Class.RPAREN)
            return True
        except:
            return False


    def parse(self):
        return self.program()

    def die(self, text):
        raise SystemExit(text)

    def die_deriv(self, fun):
        self.die("Derivation error: {}".format(fun))

    def die_type(self, expected, found):
        self.die("Expected: {}, Found: {}".format(expected, found))