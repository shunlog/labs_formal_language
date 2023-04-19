
# Table of Contents

1.  [Lab 4: Chomsky normal form](#org976db02)
2.  [Theory](#org2887f77)
3.  [Objectives](#org2611bba)
4.  [Results](#orgc912f02)
5.  [Implementation](#orgdca783b)



<a id="org976db02"></a>

# Lab 4: Chomsky normal form

-   **Course:** Formal Languages & Finite Automata
-   **Author:** Balan Artiom


<a id="org2887f77"></a>

# Theory


<a id="org2611bba"></a>

# Objectives

-   [X] Implement a method to convert a CFG to its normal form


<a id="orgc912f02"></a>

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
    
    "$$\\begin{multline}\n" + g1.to_latex() + '\n\\end{multline}$$'

$$\begin{multline}
S → A \\\\ A → d | d S | a A d A B \\\\ B → A C | a S | a C \\\\ C → ε \\\\ E → A S
\end{multline}$$


<a id="orgdca783b"></a>

# Implementation

