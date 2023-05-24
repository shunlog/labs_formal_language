#!/usr/bin/env python3
import sys
from enum import Enum, auto
from icecream import ic

class TokenType(Enum):
    EOF = auto()
    ID = auto()
    NUMBER = auto()
    INDENT = auto()
    DEDENT = auto()
    KEYWORD = auto()
    DELIMITER = auto()
    OPERATOR = auto()

keywords = {
    "False",      "await",      "else",       "import",     "pass",
    "None",       "break",      "except",     "in",         "raise",
    "True",       "class",      "finally",    "is",         "return",
    "and",        "continue",   "for",        "lambda",     "try",
    "as",         "def",        "from",       "nonlocal",   "while",
    "assert",     "del",        "global",     "not",        "with",
    "async",      "elif",       "if",         "or",         "yield"
}

delimiters = {
    "(",       ")",       "[",       "]",       "{",       "}",
    ",",       ":",       ".",       ";",       "@",       "=",       "->",
    "+=",      "-=",      "*=",      "/=",      "//=",     "%=",      "@=",
    "&=",      "|=",      "^=",      ">>=",     "<<=",     "**="
}

operators = {
    "+",       "-",       "*",       "**",      "/",       "//",      "%",      "@",
    "<<",      ">>",      "&",       "|",       "^",       "~",       ":=",
    "<",       ">",       "<=",      ">=",      "==",      "!="
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
        if p + 1 < len(s):
            return s[p:min(p+n, len(s))]
        return ""

    def prefix_in_ls(l, w):
        return any(li.find(w) == 0 for li in l)

    while True:
        # handle EOF
        if peek() == "":
            while indent_stack.pop() != 0:
                ls.append(Token(TokenType.DEDENT))
            ls.append(Token(TokenType.EOF))
            break

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
                ls.append(Token(TokenType.KEYWORD, idstr))
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

        # handle delimiters
        if prefix_in_ls(delimiters, peek()):
            i = 1
            while prefix_in_ls(delimiters, peek(i+1)) and peek(i) != peek(i+1):
                i += 1
            # some delimiters start like operators
            if peek(i) in delimiters and \
               not prefix_in_ls(operators, peek(i+1)):
                ls.append(Token(TokenType.DELIMITER, getch(i)))
                continue

        # handle operators
        if prefix_in_ls(operators, peek()):
            i = 1
            while prefix_in_ls(operators, peek(i+1)) and i < len(s):
                i += 1
            if peek(i) in operators:
                ls.append(Token(TokenType.OPERATOR, getch(i)))
                continue

        # handle comments
        if peek() == "#":
            while peek() not in ["\n", "", "\r"]:
                getch()
            continue

        # return single-character tokens as-is
        ls.append(Token(getch()))

    return ls

def main():
    inp = sys.stdin.read()
    ls = get_tokens(inp)

    from tabulate import tabulate
    tbl = tabulate([(t.type, t.value) for t in ls], tablefmt="orgtbl", headers=["Name", "Value"])
    print(tbl)

if __name__ == "__main__":
    main()
