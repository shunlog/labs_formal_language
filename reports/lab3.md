- [Implementation of formal languages](#org0306b6b)
- [Theory](#orgbbfcba4)
  - [Lexical analysis](#org4d0c301)
  - [Ambiguous grammar](#orgb02f72b)
- [Objectives](#org3e494c1)
- [Results](#org14f7fd7)
- [Implementation](#orgd917020)




<a id="org0306b6b"></a>

# Implementation of formal languages

Course
: Formal Languages &amp; Finite Automata

Author
: Balan Artiom


<a id="orgbbfcba4"></a>

# Theory


<a id="org4d0c301"></a>

## Lexical analysis

In English, words are composed of letters and words have meanings,
but the meaning isn&rsquo;t derived from the letters.
In fact, we don&rsquo;t even think of the letters when we read sentences,
we read the words as a whole and only care about their meaning.
That&rsquo;s kind of an analogy to the fact that parsers don&rsquo;t really care about the characters,
they care about syntactic units, called lexemes.

A lexeme is a string of characters that has a meaning.
Lexemes often correspond to terminals in a grammar (e.g. identifier, number, operator).

It&rsquo;s useful to store the location and length of each lexeme.
The data structure unit used to store lexemes together with information about them is called a token.


<a id="orgb02f72b"></a>

## Ambiguous grammar

Lexers for real programming languages often can&rsquo;t be constructed from the grammar alone,
since there are rules not captured in the grammar:

1.  The off-side rule (indentation-sensitive blocks) can&rsquo;t be described by context-free grammars
2.  Grammar rules can be ambiguous

When grammar rules are ambiguous, a string can be matched by multiple rules.
To counter this, for example ANTLR has disambiguating rules for tokenization ([docs](https://github.com/antlr/antlr4/blob/49b69bb31aa34654676a864b229a369680122470/doc/wildcard.md#nongreedy-lexer-subrules)):

-   Greedy and non-greedy regex lexer rules
-   Match the first rule occurring in the grammar

Ambiguous constructs should be used sparingly and in a strictly controlled fashion;
otherwise, there can be no guarantee as to what language is recognized by a parser (Aho, Alfred V and Sethi, Ravi and Ullman, Jeffrey D, 2007).

One quirk that proves disambiguization is complicated is the way ANTLR handles non-greedy rules (see rule 4 [in this section](https://github.com/antlr/antlr4/blob/49b69bb31aa34654676a864b229a369680122470/doc/wildcard.md#nongreedy-lexer-subrules)).

A token has a name and an optional value, which can be of any type (including `dict`).
Token names can correspond to nonterminals in the grammar,
but can also be groupings of terminals (e.g. &ldquo;operator&rdquo;).

Usually, whitespace doesn&rsquo;t make it past the lexer, but is still necessary to separate lexemes.
For example, `elsex` is an **idendtifier**, but `else x` is the keyword **else** and the **identifier** _x_.


<a id="org3e494c1"></a>

# Objectives

-   [X] Implement a lexer and show how it works.


<a id="org14f7fd7"></a>

# Results

Let&rsquo;s parse a simple variable assignment:

```python
a_1 = 12 * 3 + 2
```

Each token is represented by two things: a name and an optional value.
In this example, notice that the token for the variable `a` is of type `ID`,
which stands for &ldquo;identifier&rdquo;, and the token value is the name of the variable.

Similarly, numbers are represented by `NUMBER` tokens, with their value as the token value.

| Token name       | Token value   |
|------------------|---------------|
| TokenType.ID     | a<sub>1</sub> |
| =                |               |
| TokenType.NUMBER | 12            |
| \*               |               |
| TokenType.NUMBER | 3             |
| +                |               |
| TokenType.NUMBER | 2             |
| TokenType.EOF    |               |


<a id="orgd917020"></a>

# Implementation

