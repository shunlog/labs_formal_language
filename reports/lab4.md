
# Table of Contents

1.  [Lab 4: Chomsky normal form](#org58d467c)
2.  [Theory](#org7cdbd82)
3.  [Objectives](#orgadb4dc8)
4.  [Results](#org620f02a)
5.  [Implementation](#org93ba58d)



<a id="org58d467c"></a>

# Lab 4: Chomsky normal form

-   **Course:** Formal Languages & Finite Automata
-   **Author:** Balan Artiom


<a id="org7cdbd82"></a>

# Theory

The [wikipedia page](https://en.wikipedia.org/wiki/Chomsky_normal_form#DEL:_Eliminate_%CE%B5-rules) pretty much sums it up.
I can add one thing perhaps,
which is that the `DEL` procedure doesn&rsquo;t seem to handle non-terminals which only have ε-rules.
For that, I checked for such non-terminals, which I called *null* (as opposed to *nullable*),
and completely removed them from every rule.

I really wonder what was the motivation of making this the objective of the laboratory work.
Why not something more fun and practical?
This CNF thing was pretty difficult, painfully boring,
and its only use seems to be in some specific parsing algorithm (called CYK, if that matters).


<a id="orgadb4dc8"></a>

# Objectives

-   [X] Implement a method to convert a CFG to its normal form
-   [X] Write unit tests


<a id="org620f02a"></a>

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
    
    # mathjax needs doubled backslashes
    "$$" + g1.to_latex().replace('\\', '\\\\') + '$$'

$$\\begin{alignat*}{1}V_N &= \\{E,S,A,B,C\\} \\\\ V_T &= \\{a,d\\} \\\\ S &= \\{S\\} \\\\ P &= \\{ \\\\&S → A, \\\\ &A → d | d S | a A d A B, \\\\ &B → a S | A C | a C, \\\\ &C → ε, \\\\ &E → A S\\} \\\\ \\end{alignat*}$$

And here&rsquo;s its Chomsky normal form, achieved using the method I implemented:

    g1_normal = g1.to_normal_form()
    
    "$$" + g1_normal.to_latex().replace('\\', '\\\\') + '$$'

$$\\begin{alignat*}{1}V_N &= \\{E,a0,A0,d0,A2,S,A,B,S0,C,A1\\} \\\\ V_T &= \\{a,d\\} \\\\ S &= \\{S0\\} \\\\ P &= \\{ \\\\&S → d | a0 A0 | d0 S, \\\\ &A → d | a0 A0 | d0 S, \\\\ &B → a0 S | a0 A0 | d0 S | a | d, \\\\ &E → A S, \\\\ &S0 → d | a0 A0 | d0 S, \\\\ &a0 → a, \\\\ &d0 → d, \\\\ &A0 → A A1, \\\\ &A1 → d0 A2, \\\\ &A2 → A B\\} \\\\ \\end{alignat*}$$

That&rsquo;s pretty much it.

This method works with any context-free grammar
(as long as it doesn&rsquo;t have loops in the production rules I think).

I also implemented a `Grammar.is_in_normal_form` method to check if the conversion worked,
but turned out I should also somehow check if the converted grammar is equivalent to the original,
which I didn&rsquo;t, and only discovered this when testing the code manually.

Here&rsquo;s a capture of my terminal after running all the tests:

    ╰─$ coverage run -m pytest
    ========================================================= test session starts ==========================================================
    platform linux -- Python 3.10.10, pytest-7.2.0, pluggy-1.0.0
    rootdir: /home/shunlog/my_projects/angryowl
    plugins: anyio-3.6.2
    collected 55 items
    
    tests/test_all.py .......................................................                                                        [100%]
    
    ========================================================== 55 passed in 0.55s ==========================================================
    
    ╰─$ coverage report
    Name                       Stmts   Miss  Cover
    ----------------------------------------------
    src/angryowl/__init__.py       0      0   100%
    src/angryowl/automata.py      74      2    97%
    src/angryowl/grammar.py      226     20    91%
    tests/__init__.py              0      0   100%
    tests/test_all.py             83      0   100%
    ----------------------------------------------
    TOTAL                        383     22    94%


<a id="org93ba58d"></a>

# Implementation

For this laboratory work, I tried using the glorified [test-driven development](https://en.wikipedia.org/wiki/Test-driven_development) approach.
It actually was really useful.
Not only did it help me make sure I understand what I have to do before I jumped right in writing my spaghetti code,
it also allowed fragment the work into tinier functions that I could test separately.

I also used `git` much more extensively this time.
Made a branch for the feature I wanted to add (`normal_form`),
committed my changes very frequently,
and in the end squashed them all into a single large commit when the dust settled.

As for the algorithm,
I used the Wikipedia page as a reference
and simply implemented all the 5 procedures one by one,
testing each one.
&ldquo;Simply&rdquo; is lightly said,
this was one of the most difficult tasks I&rsquo;ve ever done.
I&rsquo;m still not happy with the code,
I&rsquo;m sure the tests are missing some edge-cases.
Ideally one would write all this stuff related to formal languages using formal methods,
not procedural code in a dynamic-typed language.

The new code starts at [this line](https://github.com/shunlog/angryowl/blob/master/src/angryowl/grammar.py#L206) and goes until the end of the file.
The tests [start here](https://github.com/shunlog/angryowl/blob/master/tests/test_all.py#L143).
I&rsquo;m sure there&rsquo;s a better way to structure the tests,
but I&rsquo;ll learn how to do that properly some other time.

Obviously this method handles any CF grammar,
and I have the unit tests (94% coverage btw),
so I should get both bonus points.

