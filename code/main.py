#!/usr/bin/env python3

class Grammar:
    def __init__(self, VN, VT, P, S):
        self.VN = VN
        self.VT = VT
        self.P = P
        self.S = S

    def constr_word(self):
        from random import choice
        w = self.S
        while w[-1] in self.VN:
            # There's a slight probability this will go on for too long
            N = w[-1]
            w = w[:-1] + choice(self.P[N])
        return w

    def to_FSM(self):
        fin_state = "End"

        d = {}
        for s0, rl in self.P.items():
            d |= {(s0, r[0]): r[1] if len(r) == 2 else fin_state for r in rl}

        return FSM(self.VN | {fin_state}, self.S, d, {fin_state})

class FSM:
    def __init__(self, S, s0, d, F):
        self.S = S  # states
        self.s0 = s0  # initial state
        self.d = d  # transitions
        self.F = F # finite states (subset of S)

    def verify(self, w):
        s = self.s0
        for l in w:
            ns = self.d.get((s, l))
            if not ns:
                return False
            s = ns
        return s in self.F

if __name__ == '__main__':
    # Variant #3 is non-deterministic (didn't reserve enough time for that)
    # VN=["S", "D", "R"]
    # VT=["a", "b", "c", "d", "f"]
    # P={"S": ["aS", "bD", "fR"],
    #     "D": ["cD", "dR", "d"],
    #     "R": ["bR", "f"]}
    # S = "S"

    # Variant #2
    VN = {"S", "R", "L"}
    VT = {"a", "b", "c", "d", "e", "f"}
    P = {"S": ["aS", "bS", "cR", "dL"],
         "R": ["dL", "e"],
         "L": ["fL", "eL", "d"]}
    S = "S"

    g = Grammar(VN, VT, P, S)
    fsm = g.to_FSM()

    for i in range(10):
        w = g.constr_word()
        assert(fsm.verify(w))
        assert(not fsm.verify(w+"a"))
