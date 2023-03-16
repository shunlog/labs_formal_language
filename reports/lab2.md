- [Implementation of formal languages](#orgfbc9b88)
- [Theory](#orgc0a6cbb)
- [Objectives](#orge6d91c5)
- [Results](#org9e2a654)
    - [Convert NFA to Grammar](#org36da4b3)
    - [Find out if FA is nondeterministic](#org33ae12d)
    - [Convert NFA to DFA](#org7edf659)
    - [Visualize the finite automata](#orgbea3700)
    - [Convert Grammar to NFA to DFA (lab 1)](#orge76695c)
- [Implementation](#org0866a21)




<a id="orgfbc9b88"></a>

# Implementation of formal languages

Course
: Formal Languages &amp; Finite Automata

Author
: Balan Artiom


<a id="orgc0a6cbb"></a>

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

[Automata](https://en.wikipedia.org/wiki/Automata_theory) can be used to recognize formal languages, for example described by grammars.
There are different [types of automata](https://en.wikipedia.org/wiki/Automata_theory#Types_of_automata) that can describe different types of languages.
For example:

-   A finite automaton (NFA/DFA, state machine) can describe a regular grammar (type 3)
-   A pushdown automaton (PDA) can describe a context-free grammar (type 2)

A DFA is equivalent in power to an NFA, even though NFA&rsquo;s are more flexible ([Hierarchy in terms of powers](https://en.wikipedia.org/wiki/Automata_theory#Hierarchy_in_terms_of_powers)).

-   The conversion NFA -&gt; DFA can be done using the [powerset construction](https://en.wikipedia.org/wiki/Powerset_construction).
-   The conversion regular grammar -&gt; NFA and viceversa is straightforward.
-   The conversion Grammar -&gt; DFA can&rsquo;t really be done directly,
    instead go through the steps: Grammar -&gt; NFA -&gt; DFA.


<a id="orge6d91c5"></a>

# Objectives

-   [X] Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy.
-   [X] Implement conversion of a finite automaton to a regular grammar.
-   [X] Determine whether your FA is deterministic or non-deterministic.
-   [X] Implement some functionality that would convert an NDFA to a DFA.
-   [X] Represent the finite automaton graphically (Optional, and can be considered as a bonus point):
-   [X] Document everything in the README
-   [X] Test string validation with the new more general DFA


<a id="org9e2a654"></a>

# Results

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


<a id="org36da4b3"></a>

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
q2 -> b q2 | b q3
q3 -> b q4 | a q1
q4 ->
```


<a id="org33ae12d"></a>

### Find out if FA is nondeterministic

Even though it&rsquo;s an NFA, it could be that it doesn&rsquo;t have nondeterministic transitions.
We can find that out:

```python
print(nfa.is_deterministic())
```

```text
False
```


<a id="org7edf659"></a>

### Convert NFA to DFA

```python
dfa = nfa.to_DFA()
print(dfa)
```

```text
{frozenset({'q4', 'q2', 'q3'}), frozenset({'q2'}), frozenset({'q1'}), frozenset({'q0'}), frozenset({'q2', 'q3'})}, {'a', 'b'}, {'q0'}, {(frozenset({'q0'}), 'a'): {'q1'}, (frozenset({'q1'}), 'a'): {'q2'}, (frozenset({'q1'}), 'b'): {'q1'}, (frozenset({'q2'}), 'b'): {'q2', 'q3'}, (frozenset({'q2', 'q3'}), 'a'): {'q1'}, (frozenset({'q2', 'q3'}), 'b'): {'q4', 'q2', 'q3'}, (frozenset({'q4', 'q2', 'q3'}), 'a'): {'q1'}, (frozenset({'q4', 'q2', 'q3'}), 'b'): {'q4', 'q2', 'q3'}}, {frozenset({'q4', 'q2', 'q3'})}
```

Now that we have a DFA, we can easily validate some strings according to the grammar.
But first, let&rsquo;s generate a few:

```python
l = [g.constr_word() for _ in range(5)]
print(l)
```

```text
['aabbb', 'ababbababbbababb', 'abbbabbb', 'ababbb', 'aabbbb']
```

Let&rsquo;s verify that they&rsquo;re all valid:

```python
print(all(dfa.verify(w) for w in l))
```

```text
True
```


<a id="orgbea3700"></a>

### Visualize the finite automata

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


<a id="orge76695c"></a>

### Convert Grammar to NFA to DFA (lab 1)

Extending on the previous lab task,
I can now do some things with the grammar I got:

```text
VN={S, D, R},
VT={a, b, c, d, f},
P={
    S → aS
    S → bD
    S → fR
    D → cD
    D → dR
    R → bR
    R → f
    D → d
}
```

After converting it manually to a Grammar data structure, of course:

```python
VN = {"S", "D", "R"}
VT = {"a", "b", "c", "d", "f"}
S = "S"
P = {("S",): {("a", "S"), ("b", "D"), ("f", "R")},
     ("D",): {("c", "D"), ("d", "R"), ("d")},
     ("R",): {("b", "R"), ("f")}}
g = Grammar(VN=VN, VT=VT, P=P, S=S)
```

Note that the keys in the `P` dict are tuples. Remember kids, `(A)` is not a tuple, but `(A,)` is.

Now, let&rsquo;s convert the grammar to an NFA:

```python
nfa = NFA.from_grammar(g)
print(nfa.draw('img', 'lab1_v3_nfa'))
```

![img](img/lab1_v3_nfa.gv.svg)

Hmm, looks like it&rsquo;s not deterministic because of those two &ldquo;d&rdquo; transitions from the &ldquo;D&rdquo; state. Let&rsquo;s check:

```python
print(nfa.is_deterministic())
```

```text
False
```

Yeah, it isn&rsquo;t. OK, no problem. We can just convert it to a DFA:

```python
dfa = nfa.to_DFA()
print(dfa.draw('img', 'lab1_v3_dfa'))
```

![img](img/lab1_v3_dfa.gv.svg)

Looks better!


<a id="org0866a21"></a>

# Implementation

<section id="grammar">
<h2>Grammar<a class="headerlink" href="#grammar" title="Permalink to this heading">¶</a></h2>
<dl class="py class">
<dt class="sig sig-object py" id="angryowl.grammar.Grammar">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">angryowl.grammar.</span></span><span class="sig-name descname"><span class="pre">Grammar</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">VN</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">VT</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">P</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">S</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#angryowl.grammar.Grammar" title="Permalink to this definition">¶</a></dt>
<dd><p>A grammar is represented by 4 variables:</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>VN</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.11)"><em>set</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em>) – set of nonterminals</p></li>
<li><p><strong>VT</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.11)"><em>set</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em>) – set of terminals</p></li>
<li><p><strong>P</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.11)"><em>dict</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#tuple" title="(in Python v3.11)"><em>tuple</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.11)"><em>set</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#tuple" title="(in Python v3.11)"><em>tuple</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em><em>]</em><em>]</em>) – list of productions.</p></li>
<li><p><strong>S</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a>) – starting state</p></li>
</ul>
</dd>
</dl>
<p>For example, the formal grammar:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="n">A</span> <span class="o">-&gt;</span> <span class="n">aA</span>
<span class="n">A</span> <span class="o">-&gt;</span> <span class="n">aB</span>
<span class="n">A</span> <span class="o">-&gt;</span> <span class="n">ε</span>
<span class="n">B</span> <span class="o">-&gt;</span> <span class="n">b</span>
</pre></div>
</div>
<p>Is represented by the following variables:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="n">VN</span> <span class="o">=</span> <span class="p">{</span><span class="s2">&quot;A&quot;</span><span class="p">,</span> <span class="s2">&quot;B&quot;</span><span class="p">}</span>
<span class="n">VT</span> <span class="o">=</span> <span class="p">{</span><span class="s2">&quot;a&quot;</span><span class="p">,</span> <span class="s2">&quot;b&quot;</span><span class="p">}</span>
<span class="n">P</span> <span class="o">=</span> <span class="p">{</span>
    <span class="p">(</span><span class="s2">&quot;A&quot;</span><span class="p">,):</span> <span class="p">{(</span><span class="s2">&quot;a&quot;</span><span class="p">,</span> <span class="s2">&quot;B&quot;</span><span class="p">),</span> <span class="p">(</span><span class="s2">&quot;a&quot;</span><span class="p">,</span> <span class="s2">&quot;A&quot;</span><span class="p">),</span> <span class="p">()},</span>
    <span class="p">(</span><span class="s2">&quot;B&quot;</span><span class="p">,):</span> <span class="p">{(</span><span class="s2">&quot;b&quot;</span><span class="p">,)}</span>
<span class="p">}</span>
<span class="n">S</span> <span class="o">=</span> <span class="s2">&quot;A&quot;</span>
</pre></div>
</div>
<dl class="py attribute">
<dt class="sig sig-object py" id="angryowl.grammar.Grammar.Rule">
<span class="sig-name descname"><span class="pre">Rule</span></span><a class="headerlink" href="#angryowl.grammar.Grammar.Rule" title="Permalink to this definition">¶</a></dt>
<dd><p>alias of <a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#tuple" title="(in Python v3.11)"><code class="xref py py-class docutils literal notranslate"><span class="pre">tuple</span></code></a>[<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><code class="xref py py-class docutils literal notranslate"><span class="pre">str</span></code></a>]</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="angryowl.grammar.Grammar.constr_word">
<span class="sig-name descname"><span class="pre">constr_word</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#angryowl.grammar.Grammar.constr_word" title="Permalink to this definition">¶</a></dt>
<dd><p>Assuming <em>strictly</em> right-regular grammar.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>A string built using rules from the grammar picked at random.</p>
</dd>
<dt class="field-even">Return type<span class="colon">:</span></dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)">str</a></p>
</dd>
</dl>
</dd></dl>

</dd></dl>

</section>
<section id="automata">
<h2>Automata<a class="headerlink" href="#automata" title="Permalink to this heading">¶</a></h2>
<dl class="py class">
<dt class="sig sig-object py" id="angryowl.automata.FA">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">angryowl.automata.</span></span><span class="sig-name descname"><span class="pre">FA</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">S</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">A</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">s0</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">d</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">F</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#angryowl.automata.FA" title="Permalink to this definition">¶</a></dt>
<dd><p>A finite automaton is represented by 5 variables.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>S</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.11)"><em>set</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em>) – set of states</p></li>
<li><p><strong>A</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.11)"><em>set</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em>) – alphabet, which is a set of symbols</p></li>
<li><p><strong>s0</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a>) – starting state</p></li>
<li><p><strong>d</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.11)"><em>dict</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#tuple" title="(in Python v3.11)"><em>tuple</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.11)"><em>set</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.11)"><em>set</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em><em>]</em>) – the state-transition function</p></li>
<li><p><strong>F</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.11)"><em>set</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em>) – set of final states</p></li>
</ul>
</dd>
</dl>
</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="angryowl.automata.NFA">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">angryowl.automata.</span></span><span class="sig-name descname"><span class="pre">NFA</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">S</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">A</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">s0</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">d</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">F</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#angryowl.automata.NFA" title="Permalink to this definition">¶</a></dt>
<dd><p>Each rule in the regular grammar is treated as follows:</p>
<ol class="arabic">
<li><p>A -&gt; aB</p>
<blockquote>
<div><ul class="simple">
<li><p>a transition is created: (A, a): B</p></li>
<li><p>“a” is added to the alphabet</p></li>
</ul>
</div></blockquote>
</li>
<li><p>A -&gt; a</p>
<blockquote>
<div><ul class="simple">
<li><p>a transition is created: (A, a): ε</p></li>
<li><p>a final state is added: ε</p></li>
<li><p>“a” is added to the alphabet</p></li>
</ul>
</div></blockquote>
</li>
<li><p>B -&gt; ε</p>
<blockquote>
<div><ul class="simple">
<li><p>a final state is added: B</p></li>
</ul>
</div></blockquote>
</li>
</ol>
<p>For example, the formal grammar:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="n">A</span> <span class="o">-&gt;</span> <span class="n">aA</span>
<span class="n">A</span> <span class="o">-&gt;</span> <span class="n">aB</span>
<span class="n">A</span> <span class="o">-&gt;</span> <span class="n">ε</span>
<span class="n">B</span> <span class="o">-&gt;</span> <span class="n">b</span>
</pre></div>
</div>
<p>is transformed into the following NFA:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="n">S</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;B&#39;</span><span class="p">,</span> <span class="s1">&#39;ε&#39;</span><span class="p">,</span> <span class="s1">&#39;A&#39;</span><span class="p">}</span>
<span class="n">A</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;a&#39;</span><span class="p">,</span> <span class="s1">&#39;b&#39;</span><span class="p">}</span>
<span class="n">s0</span> <span class="o">=</span> <span class="s1">&#39;A&#39;</span>
<span class="n">d</span> <span class="o">=</span> <span class="p">{(</span><span class="s1">&#39;A&#39;</span><span class="p">,</span> <span class="s1">&#39;a&#39;</span><span class="p">):</span> <span class="p">{</span><span class="s1">&#39;A&#39;</span><span class="p">,</span> <span class="s1">&#39;B&#39;</span><span class="p">},</span> <span class="p">(</span><span class="s1">&#39;B&#39;</span><span class="p">,</span> <span class="s1">&#39;b&#39;</span><span class="p">):</span> <span class="p">{</span><span class="s1">&#39;ε&#39;</span><span class="p">}}</span>
<span class="n">F</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;ε&#39;</span><span class="p">,</span> <span class="s1">&#39;A&#39;</span><span class="p">}</span>
</pre></div>
</div>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>S</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.11)"><em>set</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em>) – </p></li>
<li><p><strong>A</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.11)"><em>set</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em>) – </p></li>
<li><p><strong>s0</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a>) – </p></li>
<li><p><strong>d</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.11)"><em>dict</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#tuple" title="(in Python v3.11)"><em>tuple</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.11)"><em>set</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.11)"><em>set</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em><em>]</em>) – </p></li>
<li><p><strong>F</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.11)"><em>set</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em>) – </p></li>
</ul>
</dd>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="angryowl.automata.NFA.from_grammar">
<span class="sig-name descname"><span class="pre">from_grammar</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#angryowl.automata.NFA.from_grammar" title="Permalink to this definition">¶</a></dt>
<dd><p>This function only recognizes <em>strictly</em> regular grammars</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>g</strong> (<a class="reference internal" href="#angryowl.grammar.Grammar" title="angryowl.grammar.Grammar"><em>Grammar</em></a>) – </p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="angryowl.automata.NFA.to_DFA">
<span class="sig-name descname"><span class="pre">to_DFA</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#angryowl.automata.NFA.to_DFA" title="Permalink to this definition">¶</a></dt>
<dd><p>For an explanation of the algo, check out the dragon book.</p>
<dl class="field-list simple">
<dt class="field-odd">Return type<span class="colon">:</span></dt>
<dd class="field-odd"><p><a class="reference internal" href="#angryowl.automata.DFA" title="angryowl.automata.DFA"><em>DFA</em></a></p>
</dd>
</dl>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="angryowl.automata.DFA">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">angryowl.automata.</span></span><span class="sig-name descname"><span class="pre">DFA</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">S</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">A</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">s0</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">d</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">F</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#angryowl.automata.DFA" title="Permalink to this definition">¶</a></dt>
<dd><p>This Deterministic finite automaton is similar to the NFA,
with the distinction that states are now represented by sets, and not strings.
For example, in the transitions dict,
a value is a set of states denoting a single “node” in the DFA graph,
not multiple possible states like in the case of an NFA,
whereas the keys are now represented by tuple[set[State], Symbol]
The other variables, S, s0 and F also reflect this change.</p>
<p>For example, the NFA:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="n">S</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;B&#39;</span><span class="p">,</span> <span class="s1">&#39;ε&#39;</span><span class="p">,</span> <span class="s1">&#39;A&#39;</span><span class="p">}</span>
<span class="n">A</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;a&#39;</span><span class="p">,</span> <span class="s1">&#39;b&#39;</span><span class="p">}</span>
<span class="n">s0</span> <span class="o">=</span> <span class="s1">&#39;A&#39;</span>
<span class="n">d</span> <span class="o">=</span> <span class="p">{(</span><span class="s1">&#39;A&#39;</span><span class="p">,</span> <span class="s1">&#39;a&#39;</span><span class="p">):</span> <span class="p">{</span><span class="s1">&#39;A&#39;</span><span class="p">,</span> <span class="s1">&#39;B&#39;</span><span class="p">},</span> <span class="p">(</span><span class="s1">&#39;B&#39;</span><span class="p">,</span> <span class="s1">&#39;b&#39;</span><span class="p">):</span> <span class="p">{</span><span class="s1">&#39;ε&#39;</span><span class="p">}}</span>
<span class="n">F</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;ε&#39;</span><span class="p">,</span> <span class="s1">&#39;A&#39;</span><span class="p">}</span>
</pre></div>
</div>
<p>is transformed into the following DFA:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="n">S</span> <span class="o">=</span> <span class="p">{{</span><span class="s1">&#39;A&#39;</span><span class="p">},</span> <span class="p">{</span><span class="s1">&#39;A&#39;</span><span class="p">,</span> <span class="s1">&#39;B&#39;</span><span class="p">},</span> <span class="p">{</span><span class="s1">&#39;ε&#39;</span><span class="p">}}</span>
<span class="n">A</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;a&#39;</span><span class="p">,</span> <span class="s1">&#39;b&#39;</span><span class="p">}</span>
<span class="n">s0</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;A&#39;</span><span class="p">}</span>
<span class="n">d</span> <span class="o">=</span> <span class="p">{</span>
    <span class="p">({</span><span class="s1">&#39;A&#39;</span><span class="p">},</span> <span class="s1">&#39;a&#39;</span><span class="p">):</span> <span class="p">{</span><span class="s1">&#39;A&#39;</span><span class="p">,</span> <span class="s1">&#39;B&#39;</span><span class="p">},</span>
    <span class="p">({</span><span class="s1">&#39;A&#39;</span><span class="p">,</span> <span class="s1">&#39;B&#39;</span><span class="p">},</span> <span class="s1">&#39;a&#39;</span><span class="p">):</span> <span class="p">{</span><span class="s1">&#39;A&#39;</span><span class="p">,</span> <span class="s1">&#39;B&#39;</span><span class="p">},</span>
    <span class="p">({</span><span class="s1">&#39;A&#39;</span><span class="p">,</span> <span class="s1">&#39;B&#39;</span><span class="p">},</span> <span class="s1">&#39;b&#39;</span><span class="p">):</span> <span class="p">{</span><span class="s1">&#39;ε&#39;</span><span class="p">}</span>
<span class="p">}</span>
<span class="n">F</span> <span class="o">=</span> <span class="p">{{</span><span class="s1">&#39;A&#39;</span><span class="p">},</span> <span class="p">{</span><span class="s1">&#39;A&#39;</span><span class="p">,</span> <span class="s1">&#39;B&#39;</span><span class="p">},</span> <span class="p">{</span><span class="s1">&#39;ε&#39;</span><span class="p">}}</span>
</pre></div>
</div>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>S</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.11)"><em>set</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em>) – </p></li>
<li><p><strong>A</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.11)"><em>set</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em>) – </p></li>
<li><p><strong>s0</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a>) – </p></li>
<li><p><strong>d</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.11)"><em>dict</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#tuple" title="(in Python v3.11)"><em>tuple</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.11)"><em>set</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.11)"><em>set</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em><em>]</em>) – </p></li>
<li><p><strong>F</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#set" title="(in Python v3.11)"><em>set</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em>) – </p></li>
</ul>
</dd>
</dl>
</dd></dl>

</section>

