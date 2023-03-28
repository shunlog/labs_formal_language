#!/usr/bin/env python3
import sys
from enum import Enum, auto
from icecream import ic

class TokenType(Enum):
    EOF = auto()
    id = auto()
    number = auto()
    defn = auto()
    lparen = auto()
    rparen = auto()
    colon = auto()
    assignment = auto()

class Token:
    def __init__(self, t, v=None):
        self.type = t
        self.value = v

    def __repr__(self):
        s = "Token(" + str(self.type)
        if self.value:
            s += ", " + str(self.value)
        s += ")"
        return s

def get_token(s):
    tl = []
    p = 0
    # current character = s[p]

    if s[p] == "\n":
        p += 1
        n = 0
        while s[p] == " ":
            n += 1
            p += 1
        assert n % 4 == 0

    while s[p].isspace():
        p += 1

    if s[p].isalpha():
        idstr = ""
        while s[p+1].isalpha():
            idstr += s[p]
            p += 1

        if idstr == "def":
            return Token(TokenType.defn), p

        return Token(TokenType.id, idstr), p

    if s[p].isdigit():
        numstr = ""
        while s[p].isdigit():
            numstr += s[p]
            p += 1
        return Token(TokenType.number, int(numstr)), p-1

    if s[p] == "(":
        return Token(TokenType.lparen), p

    if s[p] == ")":
        return Token(TokenType.rparen), p

    if s[p] == ":":
        return Token(TokenType.colon), p

    if s[p] == "=":
        return Token(TokenType.assignment), p

    return s[p], p


if __name__ == "__main__":
    inp = sys.stdin.read()
    p = 0
    while p < len(inp) - 1:
        t, np = get_token(inp[p:])
        p += np + 1
        ic(t, p)
        # ic(t, p, inp[p-np-1:p])
