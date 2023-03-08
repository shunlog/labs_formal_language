#!/usr/bin/env python3
from icecream import ic
from grammar import *
from automata import *


if __name__ == '__main__':
    # Nondeterministic Regular grammar
    VN = {"A", "B"}
    VT = {"a", "b"}
    P = {("A"): {("a", "B"), ("a", "A"), ()},
        ("B"): {("b",)}}
    S = "A"

    g = Grammar(VN, VT, P, S)
    ic(g)
    ic(g.type())

    m, ml = "", 0
    for _ in range(1000):
        w = g.constr_word()
        if len(w) > ml:
            ml = len(w)
            m = w
    ic(m)
    fsm = NFA.from_grammar(g)
    ic(fsm)

    ic(fsm.is_deterministic())

    # for i in range(10):
    #     w = g.constr_word()
    #     ic(w)
    #     assert(fsm.verify(w))
    #     assert(not fsm.verify(w+"!"))
