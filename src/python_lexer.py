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

    def getch():
        nonlocal p
        ch = peek()
        p += 1
        return ch

    def peek():
        nonlocal p
        nonlocal s
        if p + 1 < len(s):
            return s[p]
        return ""

    while True:
        if peek() == "\n":
            getch()
            n = 0
            while peek() == " ":
                getch()
                n += 1

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

        while peek().isspace():
            getch()

        if peek().isalpha():
            idstr = ""
            while peek().isalpha():
                idstr += getch()

            if idstr in keywords:
                ls.append(Token(keywords[idstr]))
                continue

            ls.append(Token(TokenType.ID, idstr))
            continue

        if peek().isdigit():
            numstr = ""
            while peek().isdigit():
                numstr += getch()
            ls.append(Token(TokenType.NUMBER, int(numstr)))
            continue

        if peek() == "":
            while indent_stack.pop() != 0:
                ls.append(Token(TokenType.DEDENT))
            ls.append(Token(TokenType.EOF))
            break

        ls.append(Token(getch()))

    return ls


if __name__ == "__main__":
    inp = sys.stdin.read()
    t = get_tokens(inp)
    ic(t)
