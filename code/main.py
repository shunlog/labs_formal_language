#!/usr/bin/env python3
from icecream import ic
from grammar import *
from automata import *


if __name__ == '__main__':
    # Example Nondeterministic Regular grammar
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

    # Variant #3 NFA
    S = {"q0","q1","q2","q3","q4"}
    A = {"a","b"}
    s0 = "q0"
    F = {"q4"}
    d = {("q0","a"): "q1",
         ("q1","b"): "q1",
         ("q1","a"): "q2",
         ("q2","b"): "q2",
         ("q2","b"): "q3",
         ("q3","b"): "q4",
         ("q3","a"): "q1"}

    nfa3 = NFA(S, A, s0, F, d)

    ic(nfa3)
