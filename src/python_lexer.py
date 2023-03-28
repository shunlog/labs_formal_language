#!/usr/bin/env python3
import sys
from enum import Enum, auto
from icecream import ic

class TokenType(Enum):
    EOF = auto()
    id = auto()
    number = auto()
    defn = auto()

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

class Lexer:
    p = 0
    def __init__(self, s):
        self.s = s

    def getch(self):
        if self.p + 1 < len(self.s):
            ch = self.s[self.p]
            self.p += 1
            return ch
        return ""

    def peek(self, p=p+1):
        if self.p + 1 < len(self.s):
            return self.s[self.p]
        return ""

    def get_token(self):
        if self.peek() == "\n":
            n = 0
            while self.getch() == " ":
                n += 1
            assert n % 4 == 0

        while self.peek().isspace():
            self.getch()

        if self.peek().isalpha():
            idstr = ""
            while self.peek().isalpha():
                idstr += self.getch()

            if idstr == "def":
                return Token(TokenType.defn)

            return Token(TokenType.id, idstr)

        if self.peek().isdigit():
            numstr = ""
            while self.peek().isdigit():
                numstr += self.getch()
            return Token(TokenType.number, int(numstr))

        if self.peek() == "":
            self.getch()
            return Token(TokenType.EOF)

        return Token(self.getch())


if __name__ == "__main__":
    inp = sys.stdin.read()
    l = Lexer(inp)
    while True:
        t = l.get_token()
        ic(t)
        if t.type == TokenType.EOF:
            break
