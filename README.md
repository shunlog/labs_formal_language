- [Implementation of formal languages](#org32e78d3)
- [Objectives](#org11e68a4)
  - [Lab 1](#orge2eedf0)
  - [Lab 2](#orgc21a4c2)
    - [Convert NFA to Grammar](#org943ff29)
    - [Find out if FA is nondeterministic](#orgc6ff86e)
    - [Convert NFA to DFA](#orgd3c5887)
    - [Visualize the finite automatons](#org7a45da4)
- [Implementation](#orgbea8f81)
- [Try it out](#orgd91ae96)
- [Theory](#orgcd3733e)




<a id="org32e78d3"></a>

# Implementation of formal languages

Course
: Formal Languages &amp; Finite Automata

Author
: Balan Artiom


<a id="org11e68a4"></a>

# Objectives


<a id="orge2eedf0"></a>

## Lab 1

-   [X] Implement a  `Grammar` and a `FiniteAutomaton`, with the respective methods:
    -   `Grammar`
        -   `generateString()`
        -   `convert_to_FSM()`
    -   `FiniteAutomaton`
        -   `check_string()`
-   [X] Showcase the code:
    -   generate 5 words with the grammar
    -   create a FSM from the grammar
    -   check that the generated words are valid according to the FSM


<a id="orgc21a4c2"></a>

## Lab 2

-   [X] Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy.
-   [X] Implement conversion of a finite automaton to a regular grammar.
-   [X] Determine whether your FA is deterministic or non-deterministic.
-   [X] Implement some functionality that would convert an NDFA to a DFA.
-   [X] Represent the finite automaton graphically (Optional, and can be considered as a bonus point):
-   [X] Document everything in the README
-   [ ] Test string validation with the new more general DFA
-   [ ] REPLACE ALL GRAMMAR P DEFINITIONS HEADS TO ACTUAL TUPLES

Here&rsquo;s the NFA I got:

```text
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

```python
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

I can initialize an NFA, and then do many things with it.

```python
nfa = NFA(S=S, A=A, s0=s0, d=d, F=F)
```


<a id="org943ff29"></a>

### Convert NFA to Grammar

I can find out the type of the resulting grammar in the Chomsky hierarchy:

```python
g = nfa.to_grammar()
print(g.type())
```

```text
3
```

Or print out the grammar if I format it a bit:

```python
for l,r in g.P.items():
    print(''.join(l), '->', ' | '.join([' '.join(t) for t in r]))
```

```text
q0 -> a q1
q1 -> b q1 | a q2
q2 -> b q3 | b q2
q3 -> a q1 | b q4
q4 ->
```


<a id="orgc6ff86e"></a>

### Find out if FA is nondeterministic

Even though it&rsquo;s an NFA, it could be that it doesn&rsquo;t have nondeterministic transitions.
We can find that out:

```python
print(nfa.is_deterministic())
```

```text
False
```


<a id="orgd3c5887"></a>

### Convert NFA to DFA

```python
dfa = nfa.to_DFA()
print(dfa)
```

```text
{frozenset({'q2'}), frozenset({'q3', 'q2'}), frozenset({'q0'}), frozenset({'q3', 'q4', 'q2'}), frozenset({'q1'})}, {'b', 'a'}, {'q0'}, {(frozenset({'q0'}), 'a'): {'q1'}, (frozenset({'q1'}), 'b'): {'q1'}, (frozenset({'q1'}), 'a'): {'q2'}, (frozenset({'q2'}), 'b'): {'q3', 'q2'}, (frozenset({'q3', 'q2'}), 'b'): {'q3', 'q4', 'q2'}, (frozenset({'q3', 'q2'}), 'a'): {'q1'}, (frozenset({'q3', 'q4', 'q2'}), 'b'): {'q3', 'q4', 'q2'}, (frozenset({'q3', 'q4', 'q2'}), 'a'): {'q1'}}, {frozenset({'q3', 'q4', 'q2'})}
```

Now that we have a DFA, we can easily validate some strings according to the grammar.
But first, let&rsquo;s generate a few:

```python
l = [g.constr_word() for _ in range(5)]
print(l)
```

```text
['ababb', 'aabababbbabbabababbb', 'abbbabb', 'aababbabbbaabb', 'aabbaabaabb']
```

Let&rsquo;s verify that they&rsquo;re all valid:

```python
print(all(dfa.verify(w) for w in l))
```

```text
True
```


<a id="org7a45da4"></a>

### Visualize the finite automatons

Here&rsquo;s the NFA:

```python
fn = nfa.draw('./img', 'variant_3_nfa')
print(fn)
```

![img](img/variant_3_nfa.gv.svg)

And the DFA:

```python
fn = dfa.draw('./img', 'variant_3_dfa')
print(fn)
```

![img](img/variant_3_dfa.gv.svg)


<a id="orgbea8f81"></a>

# Implementation

I wrote very extensive comments inside source code files, so refer to those please.


<a id="orgd91ae96"></a>

# Try it out

You can starts playing inside `main.py`.

There are a few tests that you can run with `pytest`,
but they&rsquo;re not very extensive.
Also pls don&rsquo;t look inside, I&rsquo;ll refactor them I promise.


<a id="orgcd3733e"></a>

# Theory

An instance of a **formal language** is a set of _words_ which are composed of _letters_.
The set of words can be defined in many ways:

-   by simply enumerating all the valid elements (words)
-   by defining an alphabet and a grammar

An **alphabet** is a set of letters.

A **grammar** is a set of rules that define how to form valid words from the alphabet.

A regular grammar is one in which all production rules in P are of one of the following forms:

-   A → a
-   A → aB
-   A → ε

where A, B, S ∈ N are non-terminal symbols, a ∈ Σ is a terminal symbol,
and ε denotes the empty string, i.e. the string of length 0. S is called the start symbol.

