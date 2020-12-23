from enum import Enum, auto


class Class(Enum):
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    FWDSLASH = auto()
    PERCENT = auto()
    DIV = auto()
    MOD = auto()

    OR = auto()
    AND = auto()
    NOT = auto()
    XOR = auto()

    EQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()

    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()

    ASSIGN = auto()
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()

    TYPE = auto()
    INT = auto()
    CHAR = auto()
    STRING = auto()
    BOOLEAN = auto()
    REAL = auto()

    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    REPEAT = auto()
    UNTIL = auto()

    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()
    EXIT = auto()

    ADDRESS = auto()

    ID = auto()
    EOF = auto()

    BEGIN = auto()
    END = auto()
    VAR = auto()

    PROCEDURE = auto()
    FUNCTION = auto()

    OF = auto()
    TO = auto()
    DO = auto()
    ARRAY = auto()
    THEN = auto()

    DOWNTO = auto()

