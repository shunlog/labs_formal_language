# Implementation of formal languages

Course  
Formal Languages & Finite Automata

Author  
Balan Artiom

# Objectives

## Lab 1

- [x] Implement a `Grammar` and a `FiniteAutomaton`, with the respective
  methods:
  - `Grammar`
    - `generateString()`
    - `convert_to_FSM()`
  - `FiniteAutomaton`
    - `check_string()`
- [x] Showcase the code:
  - generate 5 words with the grammar
  - create a FSM from the grammar
  - check that the generated words are valid according to the FSM

## Lab 2

- [x] Provide a function in your grammar type/class that could classify
  the grammar based on Chomsky hierarchy.
- [x] Implement conversion of a finite automaton to a regular grammar.
- [x] Determine whether your FA is deterministic or non-deterministic.
- [x] Implement some functionality that would convert an NDFA to a DFA.
- [x] Represent the finite automaton graphically (Optional, and can be
  considered as a bonus point):
- [x] Document everything in the README
- [ ] Test string validation with the new more general DFA

### Results

Here's the NFA I got:

``` example
Q = {q0,q1,q2,q3,q4},
∑ = {a,b},
F = {q4},
δ(q0,a) = q1,
δ(q1,b) = q1,
δ(q1,a) = q2,
δ(q2,b) = q2,
δ(q2,b) = q3,
δ(q3,b) = q4,
δ(q3,a) = q1.
```

After manually rewriting it like this:

``` python
S = {"q0","q1","q2","q3","q4"}
A = {"a","b"}
s0 = "q0"
F = {"q4"}
d = {("q0","a"): {"q1"},
     ("q1","b"): {"q1"},
     ("q1","a"): {"q2"},
     ("q2","b"): {"q2", "q3"},
     ("q3","b"): {"q4"},
     ("q3","a"): {"q1"}}
```

I can convert it to an NFA, and then do many things with it.

``` python
nfa = NFA(S=S, A=A, s0=s0, d=d, F=F)
```

1.  Convert NFA to Grammar

    I can find out the type of the resulting grammar in the Chomsky
    hierarchy:

    Or print out the grammar if I format it a bit:

    ``` python
    for l,r in g.P.items():
        print(''.join(l), '->', ' | '.join([' '.join(t) for t in r]))
    ```

2.  Find out if FA is nondeterministic

    Even though it's an NFA, it could be that it doesn't have
    nondeterministic transitions. We can find that out:

    ``` python
    print(nfa.is_deterministic())
    ```

3.  Convert NFA to DFA

    ``` python
    dfa = nfa.to_DFA()
    print(dfa)
    ```

    Now that we have a DFA, we can easily validate some strings
    according to the grammar. But first, let's generate a few:

    ``` python
    l = [g.constr_word() for _ in range(5)]
    print(l)
    ```

    Let's verify that they're all valid:

    ``` python
    print(all(dfa.verify(w) for w in l))
    ```

4.  Visualize the finite automatons

    Here's the NFA:

    ``` python
    fn = nfa.draw('./img', 'variant_3_nfa')
    print(fn)
    ```

    And the DFA:

    ``` python
    fn = dfa.draw('./img', 'variant_3_dfa')
    print(fn)
    ```

# Implementation

I wrote very extensive comments inside source code files, so refer to
those please.

# Theory

An instance of a **formal language** is a set of *words* which are
composed of *letters*. The set of words can be defined in many ways:

- by simply enumerating all the valid elements (words)
- by defining an alphabet and a grammar

An **alphabet** is a set of letters.

A **grammar** is a set of rules that define how to form valid words from
the alphabet.

A regular grammar is one in which all production rules in P are of one
of the following forms:

- A → a
- A → aB
- A → ε

where A, B, S ∈ N are non-terminal symbols, a ∈ Σ is a terminal symbol,
and ε denotes the empty string, i.e. the string of length 0. S is called
the start symbol.
