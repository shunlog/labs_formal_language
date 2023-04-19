
# Table of Contents

1.  [Lab 4: Chomsky normal form](#orgee10f09)
2.  [Theory](#org1b036f3)
3.  [Objectives](#org7c4eee4)
4.  [Results](#org1875e41)
5.  [Implementation](#org812aecb)



<a id="orgee10f09"></a>

# Lab 4: Chomsky normal form

-   **Course:** Formal Languages & Finite Automata
-   **Author:** Balan Artiom


<a id="org1b036f3"></a>

# Theory


<a id="org7c4eee4"></a>

# Objectives

-   [X] Implement a method to convert a CFG to its normal form


<a id="org1875e41"></a>

# Results

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

$$\\begin{align}S &→ A \\\\ A &→ d S | d | a A d A B \\\\ B &→ a C | A C | a S \\\\ C &→ ε \\\\ E &→ A S\\end{align}$$


<a id="org812aecb"></a>

# Implementation

