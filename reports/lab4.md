
# Table of Contents

1.  [Lab 4: Chomsky normal form](#orgc3976a4)
2.  [Theory](#orge1cbf6c)
3.  [Objectives](#org8167cb5)
4.  [Results](#org8792c96)
5.  [Implementation](#org894cd40)



<a id="orgc3976a4"></a>

# Lab 4: Chomsky normal form

-   **Course:** Formal Languages & Finite Automata
-   **Author:** Balan Artiom


<a id="orge1cbf6c"></a>

# Theory


<a id="org8167cb5"></a>

# Objectives

-   [X] Implement a method to convert a CFG to its normal form


<a id="org8792c96"></a>

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

$$\\begin{alignat*}{1}V_N &= \\{S,B,C,A,E\\} \\\\ V_T &= \\{a,d\\} \\\\ S &= \\{S\\} \\\\ P &= \\{ \\\\&S → A, \\\\ &A → d | a A d A B | d S, \\\\ &B → a S | A C | a C, \\\\ &C → ε, \\\\ &E → A S\\} \\\\ \\end{alignat*}$$

And here&rsquo;s its Chomsky normal form:

    g1_normal = g1.to_normal_form()
    
    "$$" + g1_normal.to_latex() + '$$'

$$\\begin{alignat*}{1}V_N &= \\{A2,a0,S0,A1,E,d0,S,B,A0,C,A\\} \\\\ V_T &= \\{a,d\\} \\\\ S &= \\{S0\\} \\\\ P &= \\{ \\\\&S → d | d0 S | a0 A0, \\\\ &A → d | d0 S | a0 A0, \\\\ &B → d0 S | d | a0 S | a0 A0 | a, \\\\ &E → A S, \\\\ &S0 → d | d0 S | a0 A0, \\\\ &a0 → a, \\\\ &d0 → d, \\\\ &A0 → A A1, \\\\ &A1 → d0 A2, \\\\ &A2 → A B\\} \\\\ \\end{alignat*}$$

    g1

    {S -> A, A -> d, A -> a A d A B, A -> d S, B -> a S, B -> A C, B -> a C, C -> , E -> A S}

    from copy import deepcopy
    g2 = deepcopy(g1)
    g2._START()
    g2._TERM()
    g2._BIN()
    g2._DEL()
    g2._UNIT()
    
    g2

    {S -> d, S -> d0 S, S -> a0 A0, A -> d, A -> d0 S, A -> a0 A0, B -> d0 S, B -> d, B -> a0 S, B -> a0 A0, B -> a, E -> A S, S0 -> d, S0 -> d0 S, S0 -> a0 A0, a0 -> a, d0 -> d, A0 -> A A1, A1 -> d0 A2, A2 -> A B}


<a id="org894cd40"></a>

# Implementation

