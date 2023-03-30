- [Lab 3: A simple lexer](#org833806e)
- [Theory](#org02f4e5b)
  - [Plus-equal or plus and equal?](#org78f41b1)
  - [Keyword or identifier?](#org4b54af5)
  - [Comments](#org64f3b43)
  - [Solution: tokens](#orgdf69ee6)
- [Objectives](#org952e937)
- [Results](#orgdc58724)
- [Implementation](#org8d811a3)




<a id="org833806e"></a>

# Lab 3: A simple lexer

Course
: Formal Languages &amp; Finite Automata

Author
: Balan Artiom


<a id="org02f4e5b"></a>

# Theory

****Tokens**** within parsers correspond to ****terminal symbols**** within formal grammars.

A grammar defines how a list of _terminal symbols_ is derived from the starting non-terminal symbol.
Terminal symbols are like building blocks, which can be parsed into a tree to reason about their meaning.
Problem is, we want to write our programs as text, and not as a stream of abstract symbols.
We want text editors, not Sctratch-like GUIs.

Why can&rsquo;t we just represent terminals as strings, you ask?
Because for complex programming languages,
splitting a stream of text (e.g. a source code file) into the terminals that we meant is not trivial.


<a id="org78f41b1"></a>

## Plus-equal or plus and equal?

For example, say we have this grammar, where strings surrounded by quotes are terminal symbols.

```text
increment -> ID '+=' NUM
add -> ID '=' NUM '+' NUM
ID -> [a..z]+
NUM -> [0..9]+
```

Then, we write a short program according to this grammar:

```text
a=2+2
a+=1
```

How do you split this program into its corresponding terminals?
The first line is pretty easy:

```text
'a' '=' '2' '+' '2'
```

But the second line could be split in different ways:

```text
'a' '+' '=' '1'
```

Or

```text
'a' '+=' '1'
```

Obviously, we meant the second meaning,
but the rules of splitting a string into its corresponding terminals are not represented in the grammar,

This problem could be generalized as &ldquo;should I pick the longer string or the shorter one?&rdquo;.


<a id="org4b54af5"></a>

## Keyword or identifier?

Another problem that arises when we want to translate a text into terminals
is that sometimes a string can be interpreted as different terminals.
The most common instance of this is when keywords could be interpreted as identifiers.
For example, `break` could be either a `KEYWORD` or an `IDENTIFIER`,
since this is how an `IDENTIFIER` is usually defined:

```text
IDENTIFIER -> letter (letter|number|underscore)*
```


<a id="org64f3b43"></a>

## Comments

Yet another problem is ignoring comments inside source code.

Since comments can appear anywhere in your program (e.g. in C),
you would have to mention them everywhere in your grammar.

For example:

```text
increment -> COMMENT* ID COMMENT* '+=' COMMENT* NUM COMMENT*
add -> COMMENT* ID COMMENT* '=' COMMENT* NUM COMMENT* '+' COMMENT* NUM COMMENT*
ID -> [a..z]+
NUM -> [0..9]+
COMMENT -> '/*' [^*] '*/'
```

Hopefully you get the point, this is not at all practical.


<a id="orgdf69ee6"></a>

## Solution: tokens

It&rsquo;s clear by now that representing a terminal as a string is not viable.
The solution is to represent terminal symbols with something more abstract than strings of characters,
something unambiguous, and this something is _tokens_,

A token is usually represented by a name/type (usually an `enum` item) and a value,
which could be of any type, even a data structure holding multiple values:

-   token value
-   location in the text stream

Here is the list of tokens that the previous piece of code is supposed to encode:

```text
ID(a) EQ NUM(2) PLUS NUM(2)
ID(a) PLUSEQ NUM(1)
```

I used the notation `TOKENNAME(value)` to represent a token.

Now that we represent terminals as tokens,
we need a separate program that would translate a stream of text into these tokens.
This program is called a &ldquo;lexer&rdquo;, or &ldquo;tokenizer&rdquo;, or &ldquo;scanner&rdquo;, or whatever.

A tokenizer is naturally very ugly, since it has to handle a lot of exceptions and edge-cases:

-   intertwined comments
-   prioritize strings with multiple derivations (keyword vs. identifier)
-   decide whether to translate the longer sub-string or the shorter
-   indentation-based blocks (off-side rule)

By delegating this task to the tokenizer, the parser doesn&rsquo;t have to worry about these ugly hacks;
all it sees is a list of tokens which can be elegantly parsed according to the grammar rules alone.

It is helpful to name every single token type with an all-caps name, like here:

```text
increment -> ID PLUSEQ NUM
add -> ID EQ NUM PLUS NUM
```

However, it&rsquo;s not necessary.
Some tokens don&rsquo;t need a value, like the token `PLUS`,
so we might represent them using a simple string (like in this [Yacc grammar for C](https://www.lysator.liu.se/c/ANSI-C-grammar-y.html)).

Here&rsquo;s how a tokenizer solves the three problems described previously:

1.  Using regex notation, specify whether to do a greedy or non-greedy match
2.  prioritize keywords over identifiers by checking them for a match first
3.  Ignoring comments in a tokenizer is pretty straight-forward
4.  Bonus: indentation-based blocks can be tokenized as described in the [python docs](https://docs.python.org/3/reference/lexical_analysis.html#indentation).


<a id="org952e937"></a>

# Objectives

-   [X] Implement a lexer and show how it works.


<a id="orgdc58724"></a>

# Results

I wrote a lexer for python-like syntax, hence, all the example strings are valid python code.

Let&rsquo;s parse a simple variable assignment:

```python
a_1 += 12 * 3 + 2
```

```text
/tmp/babel-P0bk7B/python-M2mdv0
```

Each token is represented by two things: a name and an optional value.
In this example, notice that the token for the variable `a` is of type `ID`,
which stands for &ldquo;identifier&rdquo;, and the token value is the name of the variable.

Similarly, numbers are represented by `NUMBER` tokens, with their value as the token value.

| Token name            | Token value |
|-----------------------|-------------|
| `TokenType.ID`        | `a_1`       |
| `TokenType.DELIMITER` | `+=`        |
| `TokenType.NUMBER`    | `12`        |
| `TokenType.OPERATOR`  | `*`         |
| `TokenType.NUMBER`    | `3`         |
| `TokenType.OPERATOR`  | `+`         |
| `TokenType.NUMBER`    | `2`         |
| `TokenType.EOF`       |             |

Now let&rsquo;s see how a lexer recognizes indentation:

```python
def t(arg):
    print(arg)
```

| Token name            | Token value |
|-----------------------|-------------|
| `TokenType.KEYWORD`   | `def`       |
| `TokenType.ID`        | `t`         |
| `TokenType.DELIMITER` | `(`         |
| `TokenType.ID`        | `arg`       |
| `TokenType.DELIMITER` | `)`         |
| `TokenType.DELIMITER` | `:`         |
| `TokenType.INDENT`    |             |
| `TokenType.ID`        | `print`     |
| `TokenType.DELIMITER` | `(`         |
| `TokenType.ID`        | `arg`       |
| `TokenType.DELIMITER` | `)`         |
| `TokenType.DEDENT`    |             |
| `TokenType.EOF`       |             |

Did you catch that?
The lexer generated two additional &ldquo;invisible&rdquo; tokens
to let the parser know about the indented block: `INDENT` and `DEDENT`.

You could visualize the token placement like this:

```text
1. def t(arg):
     v INDENT
2.    print(arg)
3.
  ^ DEDENT
```

Let&rsquo;s see a more complicated example:

```python
if a:
    if b:
        foo()
bar()
```

| Token name            | Token value |
|-----------------------|-------------|
| `TokenType.KEYWORD`   | `if`        |
| `TokenType.ID`        | `a`         |
| `TokenType.DELIMITER` | `:`         |
| `TokenType.INDENT`    |             |
| `TokenType.KEYWORD`   | `if`        |
| `TokenType.ID`        | `b`         |
| `TokenType.DELIMITER` | `:`         |
| `TokenType.INDENT`    |             |
| `TokenType.ID`        | `foo`       |
| `TokenType.DELIMITER` | `(`         |
| `TokenType.DELIMITER` | `)`         |
| `TokenType.DEDENT`    |             |
| `TokenType.DEDENT`    |             |
| `TokenType.ID`        | `bar`       |
| `TokenType.DELIMITER` | `(`         |
| `TokenType.DELIMITER` | `)`         |
| `TokenType.EOF`       |             |

Let&rsquo;s visualize this too:

```text
1. if a:
     v INDENT
2.    if b:
          v INDENT
3.         foo()
4. bar()
  ^ 2 x DEDENT
```

Notice how two `DEDENT` tokens were generated before `bar()`,
because we &ldquo;closed&rdquo; two indented blocks.

The lexer recognizes comments too and ignores them:

```python
 # this line has a bad indent
def t(arg):
    print(arg)  # this comment is inline
```

| Token name            | Token value |
|-----------------------|-------------|
| `TokenType.KEYWORD`   | `def`       |
| `TokenType.ID`        | `t`         |
| `TokenType.DELIMITER` | `(`         |
| `TokenType.ID`        | `arg`       |
| `TokenType.DELIMITER` | `)`         |
| `TokenType.DELIMITER` | `:`         |
| `TokenType.INDENT`    |             |
| `TokenType.ID`        | `print`     |
| `TokenType.DELIMITER` | `(`         |
| `TokenType.ID`        | `arg`       |
| `TokenType.DELIMITER` | `)`         |
| `TokenType.DEDENT`    |             |
| `TokenType.EOF`       |             |

Notice that the first line has a bad indent (first line can&rsquo;t be indented in python),
but since it&rsquo;s a comment, we can ignore this issue (one more edge-case to consider).

There&rsquo;s one type of indentation error that can be recognized by the lexer (and 3 others that can only be recognized by the parser),
and that&rsquo;s the &ldquo;inconsistent dedent&rdquo;:

```python
def foo(a):
    if a == 1:
        return 1
   return 0
```

The lexer simply raises an exception for this example.

Notice how some delimiters start like operators, and viceversa:

```python
a += b == c
```

| Token name            | Token value |
|-----------------------|-------------|
| `TokenType.ID`        | `a`         |
| `TokenType.DELIMITER` | `+=`        |
| `TokenType.ID`        | `b`         |
| `TokenType.OPERATOR`  | `==`        |
| `TokenType.ID`        | `c`         |
| `TokenType.EOF`       |             |

In this case, the operator `==` starts like the delimiter `=`, and the delimiter `+=` starts like the operator `+`.
I&rsquo;m not sure what&rsquo;s the proper way to deal with this, so my code is a bit hacky.


<a id="org8d811a3"></a>

# Implementation

Indentation handling is implemented as described in the [python docs](https://docs.python.org/3/reference/lexical_analysis.html#indentation).

The entire &ldquo;lexer&rdquo; is a single function `get_tokens(s) -> ls`
that takes a string to be tokenized, and returns a list of all the tokens.

Initially I tried wrapping the tokenizer inside a class, but it didn&rsquo;t make sense
and only made things more obscure and complicated.
I don&rsquo;t see why you would need to maintain the state of a lexer by reading tokens one by one,
when you could instead get all the tokens at once.
And if you don&rsquo;t need a state, there&rsquo;s no need for an object.

The `get_tokens` function reads characters using either `getch()`  or `peek()`,
depending on whether it wants to also consume the character.

The entire function is a loop that tokenizes the entire string,
until there&rsquo;s no more characters left, after which it generates the last token, `EOF`.

