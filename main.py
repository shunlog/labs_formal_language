#!/usr/bin/env python3
from icecream import ic

from src.grammar import *
from src.automata import *


if __name__ == '__main__':
    # Variant #19 NFA
    S = {"q0","q1","q2"}
    A = {"a","b"}
    s0 = "q0"
    F = {"q2"}
    d = {("q0","a"): {"q1", "q0"},
         ("q1","b"): {"q1", "q2"},
         ("q0","b"): {"q0"},
         ("q2","b"): {"q2"},
         }

    nfa = NFA(S=S, A=A, s0=s0, d=d, F=F)
    ic(nfa)
    dfa = nfa.to_DFA()
    ic(dfa)

    fn = nfa.draw('/tmp/', 'v3nfa')
    ic(fn)
    fn = dfa.draw('/tmp/', 'v3dfa')
    ic(fn)
