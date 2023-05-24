#!/usr/bin/env python3
import sys
from icecream import ic
from lexer import *
from parser import *

if __name__ == "__main__":
    inp = sys.stdin.read()
    tokens = get_tokens(inp)
    ic(tokens)
    p = Parser()
    ast = p.parse(tokens)
    ic(ast)


    from pprint import pprint
    pprint(ast, compact=True)
