
# Table of Contents

1.  [Lab 4: Chomsky normal form](#org5e8411d)
2.  [Theory](#org1432c8f)
3.  [Objectives](#orgdf802bc)
4.  [Results](#org81c75f3)
5.  [Implementation](#orgdc56c19)



<a id="org5e8411d"></a>

# Lab 4: Chomsky normal form

-   **Course:** Formal Languages & Finite Automata
-   **Author:** Balan Artiom


<a id="org1432c8f"></a>

# Theory


<a id="orgdf802bc"></a>

# Objectives

-   [X] Implement a method to convert a CFG to its normal form


<a id="org81c75f3"></a>

# Results

Here&rsquo;s the grammar from variant #3,

    g1 = Grammar(VN = {'S', 'A', 'B', 'C', 'E'},
            VT = {'d', 'a'},
            S = 'S',
            P = {
                ('S',): {('A',)},
                ('A',): {('d',), ('d', 'S'), ('a', 'A', 'd', 'A', 'B')},
                ('B',): {('a', 'C'), ('a', 'S'), ('A', 'C')},
                ('C',): {()},
                ('E',): {('A', 'S')}})
    
    "$$" + g1.to_latex() + '$$'

$$\\begin{align}S &→ A \\\\ A &→ d | a A d A B | d S \\\\ B &→ A C | a C | a S \\\\ C &→ ε \\\\ E &→ A S\\end{align}$$

And here&rsquo;s its Chomsky normal form:

    g1_normal = g1.to_normal_form()
    
    "$$" + g1_normal.to_latex() + '$$'

$$\\begin{align}S &→ d0 S | a0 A0 | d \\\\ A &→ d0 S | a0 A0 | d \\\\ B &→ a | d0 S | a0 A0 | a0 S | d \\\\ E &→ A S \\\\ S0 &→ d0 S | a0 A0 | d \\\\ d0 &→ d \\\\ a0 &→ a \\\\ A0 &→ A A1 \\\\ A1 &→ d0 A2 \\\\ A2 &→ A B\\end{align}$$

    g1

    {S -> A, A -> d, A -> a A d A B, A -> d S, B -> A C, B -> a C, B -> a S, C -> , E -> A S}

    from copy import deepcopy
    g2 = deepcopy(g1)
    g2._START()
    g2._TERM()
    g2._BIN()
    g2._DEL()
    g2._UNIT()
    
    g2

    {S -> d0 S, S -> a0 A0, S -> d, A -> d0 S, A -> a0 A0, A -> d, B -> a, B -> d0 S, B -> a0 A0, B -> a0 S, B -> d, E -> A S, S0 -> d0 S, S0 -> a0 A0, S0 -> d, d0 -> d, a0 -> a, A0 -> A A1, A1 -> d0 A2, A2 -> A B}


<a id="orgdc56c19"></a>

# Implementation

