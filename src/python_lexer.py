#!/usr/bin/env python3
import sys
from enum import Enum, auto
from icecream import ic

class TokenType(Enum):
    EOF = auto()
    ID = auto()
    NUMBER = auto()
    DEFN = auto()
    PASS = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    INDENT = auto()
    DEDENT = auto()

keywords = {
    "def": TokenType.DEFN,
    "pass": TokenType.PASS,
    "if": TokenType.IF,
    "elif": TokenType.ELIF,
    "else": TokenType.ELSE,
}

class Token:
    def __init__(self, t, v=None):
        self.type = t
        self.value = v

    def __repr__(self):
        s = "Token[ " + str(self.type)
        if self.value:
            s += " = " + str(self.value)
        s += " ]"
        return s

def get_tokens(s: str) -> list[Token]:
    '''Tokenize a string of python source code.

    :returns: A list of all the tokens.
    '''
    p = 0
    indent_stack = [0]
    ls = []

    def getch(n=1):
        # return next character and advance
        nonlocal p
        ch = peek(n)
        p += n
        return ch

    def peek(n=1):
        # return next character without advancing
        nonlocal p
        nonlocal s
        if p + n < len(s):
            return s[p:p+n]
        return ""

    while True:

        # handle indent
        if peek() == "\n":
            getch()
            n = 0
            while peek() == " ":
                getch()
                n += 1
            # ignore commented lines
            if peek() == "#":
                while peek() not in ["\n", "", "\r"]:
                    getch()
                continue

            if n > indent_stack[-1]:
                indent_stack.append(n)
                ls.append(Token(TokenType.INDENT))
                continue

            if n < indent_stack[-1]:
                while indent_stack[-1] > n:
                    ls.append(Token(TokenType.DEDENT))
                    indent_stack.pop()
                if indent_stack[-1] != n:
                    raise(Exception)
                continue
            continue

        # ignore whitespace
        while peek().isspace():
            getch()

        # handle words
        if peek().isalpha():
            idstr = ""
            while peek().isalnum() or peek() == "_":
                idstr += getch()

            if idstr in keywords:
                ls.append(Token(keywords[idstr]))
                continue

            ls.append(Token(TokenType.ID, idstr))
            continue

        # handle numbers
        if peek().isdigit():
            numstr = ""
            while peek().isdigit():
                numstr += getch()
            ls.append(Token(TokenType.NUMBER, int(numstr)))
            continue

        # handle EOF
        if peek() == "":
            while indent_stack.pop() != 0:
                ls.append(Token(TokenType.DEDENT))
            ls.append(Token(TokenType.EOF))
            break

        # handle 2-character words
        if peek(2) in ["==", "!=", ">=", "<="]:
            ls.append(Token(getch(2)))
            continue

        # handle comments
        if peek() == "#":
            while peek() not in ["\n", "", "\r"]:
                getch()
            continue

        # return single-character tokens as-is
        ls.append(Token(getch()))

    return ls


if __name__ == "__main__":
    inp = sys.stdin.read()
    ls = get_tokens(inp)

    from tabulate import tabulate
    tbl = tabulate([(t.type, t.value) for t in ls], tablefmt="orgtbl", headers=["Name", "Value"])
    print(tbl)
