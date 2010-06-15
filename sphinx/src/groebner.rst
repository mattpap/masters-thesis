.. include:: ../globals.def

.. _thesis-groebner:

=======================================
|groebner| bases and their applications
=======================================

The method of |groebner| bases is a powerful technique for solving problems in commutative
algebra (polynomial ideal theory, algebraic geometry) that was introduced by Bruno Buchberger
in his PhD thesis [Buchberger1965thesis]_ (for English translation see [Abramson2006translation]_
and for a historical background see [Abramson2009history]_). |groebner| bases provide a uniform
approach for solving problems that can be expressed in terms of systems of multivariate polynomial
equations. It happens that many practical problems, e.g.  in operational research (graph theory),
can be transformed into sets of polynomials, thus solved using |groebner| bases method.

In this chapter we will give a short theoretical background on |groebner| bases and then we will
show, in a tutorial--like fashion on a series of examples, how to use |groebner| bases machinery
in |sympy|. After two very theoretical chapters it is time to show that polynomials manipulation
module, that we wrote for |sympy|, is actually useful for solving practical problems. We chose
|groebner| bases for this presentation, because the theory behind |groebner| bases is relatively
simple and there are many non--artificial and non--trivial examples of applications of |groebner|
bases, that can be found in literature, which do not require the reader to have extensive mathematical
knowledge, but also touch many different areas of polynomials manipulation module. However, if some
mathematical background will be needed in a particular example, then we will provide a short introduction
every time additional knowledge is needed.

Short introduction to |groebner| bases
======================================

The |groebner| bases method is a very attractive tool in computer algebra because it is a very
simple to understand and relatively simple to implement (implementation is |sympy| consists of less
than 150 lines of code) computational method. The low overhead of the theoretical background of
the principles of the |groebner| bases method (not including the proof of the main theorem, which
is, on the other hand, very complicated) makes is possible to apply |groebner| bases in various
areas of science and engineering, not only by mathematicians.

To introduce the concept of |groebner| bases, following [Buchberger2001systems]_, lets consider
a set $F$ of multivariate polynomial equations, i.e. $F = \{ f \in \K\Xn \}$, where $\K$ usually
denotes a field of characteristic zero:

#. we transform the set of polynomials $F$ into another set $G$
#. the obtained set $G$ is called a |groebner| basis of $F$
#. $G$ has some *nice* properties that the set $F$ does not posses
#. $F$ and $G$ have exactly the same sets of solutions

The |groebner| bases theory tells us that:

#. problems which are difficult to solve in terms of $F$, are *easy* to solve with $G$
#. there exists an algorithm for transforming arbitrary $F$ into an equivalent set $G$

Taking advantage of this, our approach, in the following sections, will be to understand as much as
possible about $F$ by inspecting the structure and properties of $G$. In some cases we will be given a
set of polynomial equations explicitly. Often, however, our problem will be stated in other *language*,
for example in terms of graphs or matrices, and we will need first to transform the original formulation
into a system of polynomials. Then we will be able to reason about the nature of our initial problem by
analyzing the |groebner| basis of the constructed set of polynomial.

.. _gb-construct:

Construction of |groebner| bases
================================

Suppose we are given a finite set of polynomials $F$. The question arises: how to find another set
of polynomials $G$, a |groebner| basis of $F$, such that $F$ and $G$ have the same sets of solutions?
Moreover, is it possible to find $G$ in a systematic (algorithmic) way? If so, does the algorithm
always terminate? These were tough questions as of the first half of the 20th century. However, in
1965 Bruno Buchberger in his PhD thesis gave affirmative answer to all those questions by inventing
an algorithm for constructing |groebner| bases.

The notion of s--polynomials
----------------------------

To introduce the algorithm for computing |groebner| bases, Buchberger defined first the notion of,
so called, s--polynomials. Given two multivariate polynomials $f$ and $g$, suppose that $L$ is the
least common multiple of the leading monomials of $f$ and $g$ with respect to a fixed ordering of
monomials, i.e. $L = \lcm(\LM(f), \LM(g))$, then:

.. math::

    \spoly(f, g) = \frac{L}{\LT(f)} f - \frac{L}{\LT(g)} g

where $\LT(\cdot)$ stands for the leading term and $\LM(\cdot)$ stands for the leading monomial of
a polynomial. The definition of s--polynomials can be directly transformed into Python::

    def s_polynomial(f, g):
        return expand(lcm(LM(f), LM(g))*(1/LT(f)*f - 1/LT(g)*g))

utilizing |sympy|'s built--in polynomial manipulation functions :func:`LT`, :func:`LM`, :func:`lcm`
and :func:`expand`, as well as multivariate polynomial arithmetics. For readability purpose, we
skipped in this definition important information about the ordering of polynomials. What is an
ordering of monomials? For now it is sufficient to assume that it exists and is fixed. In the
following sections we will investigate this in detail.

What is a |groebner| basis?
---------------------------

Having the definition of s--polynomials, the fundamental theorem of |groebner| bases (also known as
the Buchberger criterion) is as follows: a set of polynomials $G$ is a |groebner| basis if for all
pairs $(g_i, g_j)$ of polynomials in $G$, the remainder with respect to $G$ of the s--polynomial
of $g_i$ and $g_j$ is zero, i.e.:

.. math::

    \forall_{g_i, g_j \in G} \remainder(\spoly(g_i, g_j), G) = 0

(see [Adams1994intro]_ for details). The theorem is constructive, because the concept of
s--polynomials is well defined and as the remainder procedure we can take the *generalized
division* algorithm (also known as the *normal form* algorithm, see [Cox1997ideals]_ for a
detailed description). Given a set of polynomials $G$, one can check if $G$ is a |groebner|
basis in a finite number of steps. In |sympy|, the generalized division algorithm is implemented
in :func:`reduced` function. As an example, lets consider the following set of polynomials::

    >>> F = [f1, f2] = [x*y - 2*y, x**2 - 2*y**2]

There are only two polynomials in $F$ so it is sufficient to check just a single pair to see
if $F$ is a |groebner| basis or not. Lets apply Buchberger criterion to $f_1$ and $f_2$::

    >>> s_polynomial(f1, f2)
                3
    -2⋅x⋅y + 2⋅y

    >>> reduced(_, F)[1]
       3
    2⋅y  - 4⋅y

We computed the s--polynomial of $f_1$ and $f_2$ and the resulting remainder is non--zero, so
$F$ isn't a |groebner| basis. Lets see what will happen when we adjoin this remainder to $F$::

    >>> f3 = _
    >>> F.append(f3)

Now we have three polynomials in $F$ and three pairs to check, i.e. $(f_1, f_2)$, $(f_1, f_3)$
and $(f_2, f_3)$ (actually only the two new pairs, but lets check all three for completeness)::

    >>> s_polynomial(f1, f2)
                3
    -2⋅x⋅y + 2⋅y

    >>> reduced(_, F)[1]
    0

    >>> s_polynomial(f1, f3)
               3
    2⋅x⋅y - 2⋅y

    >>> reduced(_, F)[1]
    0

    >>> s_polynomial(f2, f3)
         2      5
    2⋅y⋅x  - 2⋅y

    >>> reduced(_, F)[1]
    0

All reductions resulted in zero reminders, so the extended $F$ is a |groebner| basis. This simple
observation leads to an algorithmic procedure for computing |groebner| bases, which we will fully
describe in :ref:`gb-toy`.

Reduced |groebner| bases
------------------------

The definition of the concept of |groebner| bases, we gave so far, has one serious flaw. Suppose we
are given two structurally distinct systems of polynomials $F$ and $F'$. We would like to know if
those systems are equivalent. We can compute |groebner| bases $G$ and $G'$ of $F$ and $F'$ respectively.
With the current definition of |groebner| bases we can't tell anything about the relation between $F$
and $F'$ by looking at $G$ and $G'$. However, the |groebner| bases theory tells us that when we compute
reduced |groebner| bases of those two systems of polynomials, then $F$ is equivalent to $F'$ if the reduced
|groebner| bases are equal, i.e. $G = G'$. This is a very strong and important result, because it allows
us to reason about systems of polynomial by looking only at their reduced |groebner| bases.

Lets now provide the definition of the concept of reduced |groebner| bases. We will reuse the generalized
division algorithm for this purpose. Given a set of polynomials $G$, which is a |groebner| basis by the
Buchberger criterion, then $G$ is a reduced |groebner| basis when the following statement holds:

.. math::

    \forall_{g \in G} \remainder(g, G - \{g\}) = g \wedge g\;\mbox{is monic}

Following this definition, given a |groebner| basis $G$, one can compute a reduced version of $G$
simply by reducing each element $g \in G$ with respect to all other elements of the basis and, in
the end, making all polynomials in $G$ monic. In the remainder of this chapter we will focus only
on reduced |groebner| bases.

.. _gb-toy:

Toy Buchberger algorithm
------------------------

We are ready to describe the Buchberger algorithm. The algorithm proceeds as follows: take a
set of polynomials $F$ and set initially $G := F$, where $G$ will be the desired |groebner|
basis of $F$ at the and of this procedure. Next apply the Buchberger criterion to see if
$G$ is already a |groebner| basis. If this is the case, reduce each polynomial in $G$ with
respect to other polynomials in $G$ and stop. Otherwise pick a pair of polynomials $f_1$ and
$f_2$ from $G$, and compute their s--polynomial. If the remainder with respect to $G$ of the
s--polynomial is non--zero, then adjoin it to $G$. Iterate until $G$ is a |groebner| basis.

This simple procedure can be easily coded in Python in just a couple of minutes using previously
defined :func:`s_polynomial` and |sympy|'s built--in :func:`reduced` functions::

    def buchberger(F, reduced=True):
        """Toy implementation of Buchberger algorithm. """
        G, pairs = list(F), set([])

        for i, f1 in enumerate(F):
            for f2 in F[i+1:]:
                pairs.add((f1, f2))

        while pairs:
            f1, f2 = pairs.popitem()

            s = s_polynomial(f1, f2)
            _, h = reduced(s, G)

            if h != 0:
                for g in G:
                    pairs.add((g, h))

                G.append(g)

        if reduced:
            for i, g in enumerate(G):
                _, G[i] = reduced(g, G[:i] + G[i+1:])

            G = map(monic, G)

        return G

Lets analyze :func:`buchberger` step--by--step. As the first step we assign $G$ with the input
system of polynomial equations $F$ and generate a set with all (unordered) pairs of polynomials
from $F$. We will use this set to verify the Buchberger criterion for $G$. Next we enter a loop,
which will execute until there are *critical* pairs to check. If there are no more pairs, then
the Buchberger criterion is satisfied and $G$ is a |groebner| basis. In the loop, we take a pair
of polynomials $f_1$ and $f_2$, and compute their s--polynomial and its reduction with respect
to the current basis. If the reduction is non--zero, we adjoin new element to $G$ and update
the set of *critical* pairs. When the loop terminates we obtain a |groebner| basis of $F$. In
the final step of the algorithm, if ``reduced`` flag is set, we reduce each element of the basis
with respect to other elements and make each element monic, obtaining a reduced |groebner| basis.

As it was done with the definition of the function for computing s--polynomials, also in this case
we simplified the implementation by skipping additional information about the ordering of monomials.
This is not an issue, because |sympy| assumes *lexicographic* ordering by default and allows to use
*context managers* for configuring ordering post facto.

Termination of the algorithm
----------------------------

Although the Buchberger algorithm is very simple, its termination isn't trivial. At the startup
of this procedure there is only a finite number of pairs of polynomials for which the corresponding
s--polynomials have to be computed. Some of those pairs lead to non--zero reductions, hence $G$ is
growing and the number of additional pairs, that have to be taken into consideration, also grows.
Buchberger proved that this process ends in a finite number of steps. Thus we are guaranteed that
for arbitrary set of polynomials we can compute a corresponding |groebner| basis in finite time.
An interesting question arises: how much time is actually needed to compute such a basis? We will
postpone answer to this question till the end of chapter, where we will discuss complexity of the
Buchberger algorithm and efficiency of |sympy|'s |groebner| bases implementation.

Computing |groebner| bases with |sympy|
=======================================

Although the toy implementation of the Buchberger algorithm, presented in the previous section, can
be used for experimenting with |groebner| bases, its implementation is too naive to make it useful
for solving more complicated problems. For the purpose of computing reduced |groebner| bases with
respect to various orderings of monomials, |sympy| has a built--in function :func:`groebner`, which
implements a much more efficient version of Buchberger algorithm.

The main difference between those two implementations is that :func:`groebner` uses several criteria
for cutting down the number of polynomial divisions (actually reductions by a set of polynomials), which
are the central and most expensive part of the Buchberger algorithm. There wouldn't be nothing special
about this, however, most divisions give zero remainder as the result and do not lead to change of
a |groebner| basis. This way most divisions are just *useless* and an efficient implementation of the
Buchberger algorithm must accommodate for this, avoiding as many of those useless divisions as possible.

Several criteria were invented by the author of the |groebner| bases method a few years after the
algorithm was introduced. Later on, other more powerful elimination criteria were developed, for
example, heuristic criteria for lexicographic ordering of monomials [Czapor1991heuristic]_ or, so
called, *sugar flavour* (see [Giovini1991sugar]_ for details).

.. _thesis-orderings:

Admissible orderings of monomials
=================================

The main reason for our interest in |groebner| bases is that they have *nicer* properties, compared
to other systems of polynomials. Depending on what properties we actually need, we can compute a
|groebner| basis of a given system with respect to a specific ordering of monomials. The choice of
monomial order is significant, because different orderings will lead to different properties of the
resulting basis. Moreover, for a particular system of polynomials, one ordering will make computations
feasible, whereas another will make Buchberger algorithm executing for ages. In the following sections
we will give examples showing why the right choice of monomial order is so important.

There are currently three admissible orderings of monomials implemented in |sympy|:

    **lex**
        pure lexicographic order
    **grlex**
        total degree order with ties broken by lexicographic order
    **grevlex**
        total degree order with ties broken by reversed lexicographic order

Ordering of monomials can be given to :func:`groebner` using ``order`` keyword argument. The default
is ``lex`` order, as it is the most frequently used monomial order, because it leads to, so called,
*elimination* property. The specification of the required ordering of monomials can be passed as a
string via ``order`` keyword or as a single argument function. The other option gives the possibility
of inventing our own orderings of monomials. In this case, however, |sympy| won't check if the given
function defines an admissible ordering or not.

Suppose we have a system of two bivariate polynomials ``f1, f2 = [2*x**2*y + x*y**4, x**2 + y + 1]``.
We can inspect the leading terms with respect two different orderings of monomials of a polynomial with
assistance of :func:`LT` function::

    >>> LT(f1, x, y, order='lex')
       2
    2⋅x ⋅y

    >>> LT(f1, x, y, order='grlex')
       4
    x⋅y

Similarly as in :func:`groebner` function, :func:`LT` assumes *lexicographic* ordering  of monomials by
default. We observe, in the above example, that :func:`LT` picks up different terms depending on the
chosen ordering. This happens, because in the case of ``grlex`` ordering the total degree of a monomial
is more important than the sequence exponents of that monomial. Differences between leading terms computed
by :func:`LT` influence computations of |groebner| bases::

    >>> groebner([f1, f2], x, y, order='lex')
    ⎡                   7    4                                          ⎤
    ⎢ 2                y    y       2         8    7      3      2      ⎥
    ⎢x  + y + 1, x⋅y + ── + ── + 2⋅y  + 2⋅y, y  + y  + 4⋅y  + 8⋅y  + 4⋅y⎥
    ⎣                  2    2                                           ⎦

    >>> groebner([f1, f2], x, y, order='grlex')
    ⎡   4      2             2            5    4   2        ⎤
    ⎣x⋅y  - 2⋅y  - 2⋅y, 2⋅x⋅y  + 2⋅x⋅y + y  + y , x  + y + 1⎦

Originally orderings of monomials were implemented as comparison functions and passed to :func:`sorted`
built--in function via ``cmp`` keyword argument. This approach was inefficient, because the nature of
the sorting algorithm required to compute ordering information (e.g. total degree) about a particular
monomial multiple times in this scheme. Eventually, ``cmp``--style sorting was dropped in Python 3.0,
in favour of ``key``--based sorting [PythonIssue1771]_. The new implementation of orderings of monomials
is based on the concept of ``key``--functions. When implementing user defined orderings, one must conform
to the new approach.

In principle, in the ``key``--based approach, one has to return all required ordering information about
a particular monomial in a form of tuple (with correct order of elements). In the case of *lexicographic
ordering* of monomials, this information simply consists of the input monomial itself::

    def monomial_lex_key(monom):
        """Key function for sorting monomials in lexicographic order. """
        return monom

The above is an exact excerpt from ``sympy/polys/monomialtools.py``, where orderings of monomials are
implemented. In the case of *graded lexicographic ordering* we have an additional information, which is
the total degree of an input monomial, so the key function for ``grlex`` order is defined as follows::

    def monomial_grlex_key(monom):
        """Key function for sorting monomials in graded lexicographic order. """
        return (sum(monom), monom)

This approach generalizes to other orderings as well. One should also note that the order variables is
also an important factor when computing |groebner| bases, as there are $n!$ specific orderings for a
given ordering of monomials (where $n$ is the number of variables involved in computations).

Specialization of |groebner| bases
==================================

The |groebner| bases algorithm specializes to:

1. *Gauss' algorithm* for linear polynomials
2. *Euclid's algorithm* for univariate polynomials

Special case 1: Gauss' algorithm
--------------------------------

Lets consider the following system of linear equations:

.. math::

    \left\{
    \begin{array}{rcl}
       x + 5 y &=& 2    \\
    -3 x + 6 y &=& 15
    \end{array}
    \right.

which can be written in Python as::

    >>> F = [x + 5*y - 2, -3*x + 6*y - 15]

It's a simple system, so it can be solved by hand. We can, however, use |groebner| bases
machinery to solve this system algorithmically::

    >>> groebner(F, x, y)
    [x + 3, y - 1]

As the result we got a list of two polynomials. From te list we can obtain the solution
of the system, which is $x = -3$ and $y = 1$ in this case. The same can be computed using
a much more traditional tool in the field of linear algebra, mainly using Gauss--Jordan
algorithm::

    >>> solve(F, x, y)
    {x: -3, y: 1}

We obtained the same solution but in the dictionary form this time. It's interesting to
notice that currently, at least for small inputs, the |groebner| bases approach is much
efficient than a specialized solver. Lets compare those two methods::

    >>> %timeit groebner(F, x, y)
    100 loops, best of 3: 5.15 ms per loop

    >>> %timeit solve(F, x, y)
    10 loops, best of 3: 22.7 ms per loop

An explanation of this result is as follows: |groebner| bases utilize very efficient core
of polynomials manipulation module, whereas :func:`solve` uses inefficient implementation
of linear algebra in |sympy|. This situation will change and the observed phenomenon will
disappear in near future, when linear algebra module will be refactored (using similar
approach to what was done with polynomials manipulation module).

.. _thesis-euclid:

Special case 2: Euclid's algorithm
----------------------------------

Lets now focus on the other case, i.e. on computation of greatest common divisors of polynomials.
For this, consider two univariate polynomials ``f`` and ``g``, both in the indeterminate ``x``,
with coefficients in the ring of integers::

    >>> f = expand((x - 2)**3 * (x + 3)**4 * (x + 7))
    >>> g = expand((x + 2)**3 * (x + 3)**3 * (x + 7))

We can easily see that those polynomials have to factors in common (of multiplicity three
and one respectively). Lets verify this observation using |groebner| bases algorithm::

    >>> groebner([f, g])
    ⎡ 4       3       2              ⎤
    ⎣x  + 16⋅x  + 90⋅x  + 216⋅x + 189⎦

We obtained a polynomial of degree four which clearly verifies observation concerning
multiplicities of the commons factors of ``f`` and ``g``. Lets add more structure to
the computed polynomial GCD using factorization::

    >>> factor(_[0])
           3
    (x + 3) ⋅(x + 7)

Now we can clearly see the common factors of the input polynomials. Although utilization of
|groebner| bases algorithm for computing GCDs of univariate polynomials is very fancy, there
are much more efficient algorithms for this purpose. In |sympy| we currently use heuristic GCD
algorithm over integers and rationals, and subresultants over other domains.

Moreover, |groebner| bases can be used to compute greatest common divisors of multivariate
polynomials [Cox1997ideals]_. The algorithm reduces the problem of finding the GCD of two
multivariate polynomials, say ``f`` and ``g``, into the problem of finding their least
common multiple. The final result is obtained using the well known formula that relates
GCD with LCM:

.. math::
    :label: gcdlcm

    \gcd(f, g) = \frac{f \cdot g}{\lcm(f, g)}

The multivariate polynomial LCM is computed as the unique generator of the intersection of
the two ideals generated by ``f`` and ``g``. The approach is to compute a |groebner| basis
of $t \cdot f$ and $(1 - t) \cdot g$, where $t$ is an unrelated variable, with respect to
lexicographic order of terms which eliminates $t$. The polynomial LCM of ``f`` and ``g``
is the last element of the computed |groebner| basis.

As an example consider the following two bivariate polynomials over integers::

    >>> f = expand((x - 1)**3 * (x + y)**4 * (x - y))
    >>> g = expand((x + 1)**3 * (x + y)**3 * (x - y))

To compute the GCD of ``f`` and ``g`` we will introduce new variable $t$ and then we will
find a |groebner| basis of $t \cdot f$ and $(1 - t) \cdot g$ which eliminates $t$::

    >>> basis = groebner([t*f, (1 - t)*g], t, x, y)

Note that the order of variables is significant. We chose $t$ to be of higher rank than
$x$ or $y$ to allow |groebner| basis algorithm to eliminate it from the last element of
the basis. As the relative rank of $x$ and $y$ is not important in this case, we can
rewrite the above expression in a slightly different form::

    >>> basis = groebner([t*f, (1 - t)*g], wrt=t)

This syntax signifies that the only important knowledge here is that $t$ comes before
any other variable. This approach is also far more general because we could use input
polynomials with more variables without changing the algorithm, as long as there is no
clash of variables with $t$. We can guarantee that this won't happen by declaring $t$
as a *dummy* variable, i.e. ``t = Symbol('t', dummy=True)``.

Also one should note that we didn't specify the order of terms in |groebner| basis
computation. As we use *lexicographic* order for computing the LCM of ``f`` and ``g``
we need to provide no further information, because all algorithms in polynomials
manipulation module use *lexicographic* order of terms by default.

Given a |groebner| basis of the ideal generated by ``f`` and ``g``, the last element
of this basis is the desired LCM. By using formula :eq:`gcdlcm` we can compute the
greatest common divisor of the input polynomials::

    >>> quo(f*g, basis[-1])
     4        3        3    4
    x  + 2⋅y⋅x  - 2⋅x⋅y  - y

    >>> factor(_)
           3
    (x + y) ⋅(x - y)

We obtained the correct GCD of ``f`` and ``g``. As in the univariate case, the same
result can computed, thought much more efficiently, using :func:`gcd` function, which
utilizes specialized algorithms for computing greatest common divisors.

Historically this was the first algorithm for computing GCDs of multivariate polynomials
in |sympy|. Although it's not a very efficient approach to the problem, it can serve as a
good explanation of |groebner| bases machinery. Currently we use heuristic GCD algorithm
for the task and there are plans to implement EEZ algorithm for this task.

Applications of |groebner| bases
================================

In the previous section we saw a few examples of applications of |groebner| bases, which one may
consider a little artificial. This was, however, just a short prelude to the true importance of
the |groebner| bases method. Over the years, |groebner| bases theory gained a lot of attention
outside the mathematical community and applications for it have been found in many areas of science
and engineering. Bruno Buchberger, the inventor of |groebner| bases algorithm, deserves a lot of
credit for this state of art, because of his many publications and books which popularized the method
in scientific and engineering communities. Following [Buchberger1998applications]_, below we present
a list, thought incomplete, of the major areas in which |groebner| bases were applied with great success:

* Algebraic Geometry
* Coding Theory
* Cryptography
* Invariant Theory
* Integer Programming
* Graph Theory
* Statistics
* Symbolic Integration
* Symbolic Summation
* Differential Equations
* Systems Theory

In [Buchberger2001systems]_ there is an even longer list of applications specific to systems theory.
In the following subsections we will examine several practical applications of the |groebner| bases
method and explain how to conduct all computations using |sympy|'s polynomials manipulation module.

Solving systems of polynomial equations
---------------------------------------

In the previous section we showed that |groebner| bases can be used for solving systems
of linear equations. This is an interesting, although not very useful result because we
have specialized algorithms for the task. However, |groebner| bases can used to tackle
much more complicated problem: finding solutions of systems of *polynomial* equations.

To accomplish this we will utilize a very fruitful property of |groebner| bases: elimination
property. Following [Buchberger2001systems]_ and [Adams1994intro]_, suppose $F$ is a set of
polynomial equations, such that every element of $F$ belongs to $\K\Xn$, where $\K$ is a field
of positive characteristic, and $G$ is its |groebner| computed with respect to any *elimination*
ordering of terms (e.g. lexicographic ordering). We assume that $x_1 \succ \ldots \succ x_n$. Then
$F$ and $G$ generate the same ideal, so they have the same set of solutions. The elimination property
of |groebner| bases guarantees that if $G$ has only a finite number of solutions then $G$ has exactly
one polynomial in $x_n$, i.e. a univariate polynomial which can solved. As :func:`groebner` returns
a sorted basis, the univariate polynomial will be the last element the basis.

In principle the algorithm works as follows: given a set of polynomial equations $F$ we compute
its |groebner| basis $G$ with respect to lexicographic term order. If $G$ has only one univariate
polynomial then we solve it, e.g. by radicals (if possible), and substitute the solutions back to
$G$, skipping the univariate polynomial we already solved, obtaining a set of smaller polynomial
systems. If the system doesn't have finite number of solutions we output ``failed`` or fallback
to other methods. We continue this method recursively until we find all solutions for all variables
of the initial system.

To illustrate this process, lets consider a simple bivariate example::

    >>> F = [x*y - 2*y, x**2 - 2*y**2]

We compute a lexicographic |groebner| basis of $F$ assuming that $y \succ x$::

    >>> G = groebner(F, wrt=y)

    >>> G
    ⎡   2                           ⎤
    ⎢  x     2              3      2⎥
    ⎢- ── + y , x⋅y - 2⋅y, x  - 2⋅x ⎥
    ⎣  2                            ⎦

As the last element of the basis we obtained a univariate polynomial in $x$, confirming what
the theory predicted. We can easily solve this polynomial using :func:`roots` function::

    >>> roots(_[-1])
    {0: 2, 2: 1}

We obtained three solutions: $x_1 = 0$, $x_2 = 0$ and $x_3 = 2$. We can substitute them back
into the computed |groebner| basis $G$. We are guaranteed that the resulting polynomials in
each new system will have a nontrivial greatest common divisor. Lets take $x_1$ (the same
will follow for $x_2$)::

    >>> [ g.subs(x, 0) for g in G ]
    ⎡ 2         ⎤
    ⎣y , -2⋅y, 0⎦

    >>> groebner(_, y)
    [y]

So we obtained a solution of $F$, mainly $(x, y) = (0, 0)$ of multiplicity $2$, because
$x_1 = x_2$. The necessity to specify $y$ in the above computation comes from the fact
that currently expression parsing is done independently for each polynomial in the input
system, so without $y$ the function would complain that it doesn't know how to construct
a polynomial from $0$. As we know from the previous section, the |groebner| basis algorithm
is equivalent to GCD computation in the univariate case, so we could have computed GCD of
``[y**2, -2*y, 0]`` as well to obtain the same result.

Similarly we can can substitute $x_3$ for $x$ in $G$ obtaining::

    >>> [ g.subs(x, 2) for g in G ]
    ⎡ 2          ⎤
    ⎣y  - 2, 0, 0⎦

We got a single univariate polynomial which we can solve by radicals::

    >>> roots(_[0])
    ⎧  ___        ___   ⎫
    ⎨╲╱ 2 : 1, -╲╱ 2 : 1⎬
    ⎩                   ⎭

So the remaining two solutions are $(2, \sqrt{2})$ and $(2, -\sqrt{2})$. This way we found
all solutions of $F$. This was simple example. In more complicated ones we would need to
compute |groebner| bases recursively after each substitution.

An algorithm for solving systems of polynomial equations was implemented in polynomials
manipulation module in |sympy|, so we can compute solutions of $F$ issuing a single command::

    >>> solve(F)
    ⎡        ⎛      ___⎞  ⎛     ___⎞⎤
    ⎣(0, 0), ⎝2, -╲╱ 2 ⎠, ⎝2, ╲╱ 2 ⎠⎦

Note that only unique solutions are returned by :func:`solve`. One should also remember that
only systems with finite number of solutions can be handled using |groebner| bases approach.
Suppose we form a new system of polynomial equations $G$ by multiplying $F$ element--wise by
a third variable, say $t$, i.e. ``G = [ t*f for f in F ]``. Then $G$ has infinite number of
solutions, because both polynomials in the system are homogeneous and if $t = 0$ then we can
choose arbitrary values for $x$ and $y$. If $G$ was given as input to :func:`solve`, then it
would result in :exc:`NotImplementedError` exception. Support for solving of systems of
polynomial equations with infinite number of solutions is a subject for implementation
in future versions of |sympy|.

Lets back for a moment to the point where we were computing the |groebner| basis of $F$. We
did the computation with respect to $y$, i.e. assuming $y \succ x$. Now we will compute the
|groebner| basis of $F$ the other way::

    >>> groebner(F, wrt=x)
    ⎡ 2      2              3      ⎤
    ⎣x  - 2⋅y , x⋅y - 2⋅y, y  - 2⋅y⎦

As expected, we got a univariate polynomial in $y$, however, a different one::

    >>> roots(_[-1])
    ⎧        ___        ___   ⎫
    ⎨0: 1, ╲╱ 2 : 1, -╲╱ 2 : 1⎬
    ⎩                         ⎭

Previously we got three rational solutions, so after substitution we got polynomials with
rational coefficients and, as a consequence, we could use more efficient algorithms. Now
we run into a little trouble because we will have to carry those square roots all along
our computations. We can't actually complain about this because this is the nature of the
problem we are solving and we were just lucky in the previous case, where algebraic numbers
were introduced at the very end.

There is a method of [Strzebonski1997computing]_ to avoid computing with algebraic numbers, which
requires enlarging of the input polynomial system to :func:`groebner`. Instead of substituting
an algebraic number for a variable, we can instead substitute a *dummy* variable for it and add
the minimal polynomial of the algebraic number to the system of equations. This way we have
a simpler coefficient domain but a larger system we pass to the |groebner| basis algorithm.
Currently this approach isn't implemented is |sympy| although seems promising for future use.

Algebraic relations in invariant theory
---------------------------------------

Many problems in applied algebra have symmetries or are invariant under certain natural
transformations. In particular, all geometric magnitudes and properties are invariant with
respect to the underlying transformation group, e.g. properties in Euclidean geometry are
invariant under the Euclidean group of rotations [Sturmfels2008invariant]_. Analysis of
this structure can give a deep insight into the studied problem.

Following [Buchberger2001systems]_ and [Sturmfels2008invariant]_ lets consider the group $\Z_4$
of rotational symmetries in the counter clockwise direction of the square. The invariant ring of
this group is equal to:

.. math::

    \mathcal{I} = \left\{ f \in \C[x_1, x_2] : f(x_1, x_2) = f(-x_2, x_1) \right\}

This ring has three fundamental invariants:

.. math::

    \begin{array}{ccc}
    I_1 = x_1^2 + x_2^2, & I_2 = x_1^2 x_2^2, & I_3 = x_1^3 x_2 - x_1 x_2^3
    \end{array}

Polynomials $I_1$, $I_2$ and $I_3$ form a basis of $I$ and all other polynomials in $I$
can be expressed in terms of them. The first question we may ask in algorithmic invariant
theory is what algebraic dependence relation do $I_1$, $I_2$ and $I_3$ satisfy. In other
words, we would like to find a polynomial $f(i_1, i_2, i_3)$ such that $f(I_1, I_2, I_3)
\equiv 0$. For this purpose we can use |groebner| bases algorithm utilizing, so called,
*slack variable* approach. We introduce three slack variables $i_1$, $i_2$ and $i_3$,
construct a system of polynomial equations $F = \{I_1 - i_1, I_2 - i_2, I_3 - i_3\}$
and compute |groebner| basis of $F$ with respect to lexicographic term order eliminating
$x_1$ and $x_2$. Lets see how this can be accomplished in |sympy| using polynomials
manipulation module. First we introduce all the necessary variables and the three
fundamental invariants of $\mathcal{I}$::

    >>> var('x1,x2,i1,i2,i3')
    (x₁, x₂, i₁, i₂, i₃)

    >>> I1 = x1**2 + x2**2
    >>> I2 = x1**2*x2**2
    >>> I3 = x1**3*x2 - x1*x2**3

Next we construct $F$, i.e. define ``F = [I1 - i1, I2 - i2, I3 - i3]``, and finally we
compute lexicographic |groebner| basis of $F$ eliminating $x_1$ and $x_2$::

    >>> G = groebner(F, wrt='x1,x2')

As |groebner| bases computed by :func:`groebner` function are unique and sorted by
decreasing leading monomials, we obtain the desired algebraic dependence relation
between $I_1$, $I_2$ and $I_3$ as the last element of ``G``::

    >>> G[-1]
      2          2     2
    i₁ ⋅i₂ - 4⋅i₂  - i₃

We can verify that this relation is true by substitution, i.e. if we substitute the
fundamental invariants for the slack variables, the above polynomial should vanish::

    >>> _.subs({i1: I1, i2: I2, i3: I3}).expand()
    0

As the result ``G[-1]`` is correct algebraic dependence relation between the fundamental
invariants of $\mathcal{I}$. In this example we learnt another syntax for eliminating
variables using ``wrt`` keyword argument. In previous sections we eliminated just a single
variable with its help, however, in general we can pass arbitrary number of variables via
``wrt``, either by setting it to a string consisting of a sequence of comma separated
variables separated or as on ordered container of variables (e.g. ``list`` or ``tuple``).

When introducing polynomials $I_1$, $I_2$ and $I_3$ it was stated that those polynomials
form a basis for all other polynomials in the ring of rotations of the square. So another
question we may ask is if some polynomial, say $g$ can be expressed in terms of those three
polynomials. Lets consider a polynomial $g = x_1^7 x_2 - x_1 x_2^7$. We want to find a
polynomial $f(i_1, i_2, i_3)$ such that $f(I_1, I_2, I_3) = g$. For this purpose we will
use |groebner| bases approach once again, by reusing previously computed basis $G$. What
remains to do is to reduce the polynomial $g$ with respect to the set $G$ utilizing, as
previously, lexicographic term order eliminating $x_1$ and $x_2$. The reduction of polynomial
by a set of polynomials is accomplished by taking the remainder from the result given by the
generalized multivariate polynomial division algorithm (also known as normal form algorithm)
which is implemented in :func:`reduced` function::

    >>> reduced(x1**7*x2 - x1*x2**7, G, wrt=[x1, x2])[1]
      2
    i₁ ⋅i₃ - i₂⋅i₃

We obtained a polynomial with $x_1$ and $x_2$ eliminated which means that $g$ can be written
in terms of the generators of $\mathcal{I}$ and the above polynomial is the representation of
$g$. As previously, the correctness of this result can be verified by substitution::

    >>> _.subs({i1: f1, i2: f2, i3: f3}).expand()
      7           7
    x₁ ⋅x₂ - x₁⋅x₂

If we take another polynomial, e.g. $g' = x_1^6 x_2 - x_1 x_2^6$, then::

    >>> _, f = reduced(x1**6*x2 - x1*x2**6, G, wrt=[x1, x2])

    >>> f.has(x1, x2)
    True

which means that :func:`reduced` wasn't able to eliminate $x_1$ and/or $x_2$ from $g'$ and,
as a consequence, $g'$ has no representation in terms of the generators of $\mathcal{I}$,
i.e. $g'$ doesn't belong to $\mathcal{I}$ as $g'(x_1, x_2) \not= g'(-x_2, x_1)$.

Note that in this example we used the list variant of ``wrt`` keyword argument. Likewise in the
case of computing a |groebner| basis, :func:`reduced` assumes by default lexicographic order of
terms, so there was no need to specify this explicitly. In the following section we will see that
other orderings, e.g. degree orderings, are also very useful.

|groebner| bases proved useful for finding algebraic relations between polynomials in the general
case. There is, however, a special case for which usage of the |groebner| bases method would be an
overkill. Given a symmetric polynomial we ask if it is possible to express this polynomial in terms
of elementary symmetric polynomials. For this task, called symmetric reduction, :func:`symmetrize`
function was implemented. :func:`symmetrize` takes a polynomial $f$ (not necessarily symmetric) and
returns a tuple consisting of the symmetric part of $f$, which is expressed as a combination of
elementary symmetric polynomials, and the non--symmetric part (called remainder). Consider a
bivariate polynomial $f = x^2 + y^2$. Lets compute symmetric reduction of $f$::

    >>> symmetrize(x**2 + y**2)
    ⎛                2   ⎞
    ⎝-2⋅x⋅y + (x + y) , 0⎠

As the resulting remainder is zero, we proved that $f$ is a symmetric polynomial. :func:`symmetrize`
was also able to rewrite $f$ in terms of bivariate elementary symmetric polynomials $s_1 = x + y$ and
$s_2 = x y$. To make this more visible, we can force :func:`symmetrize` to return results in a *formal*
form::

    >>> symmetrize(x**2 + y**2, formal=True)
    ⎛  2                                ⎞
    ⎝s₁  - 2⋅s₂, 0, {s₁: x + y, s₂: x⋅y}⎠

This way we can clearly see the two elementary symmetric polynomials in the result. To show that the
result from :func:`symmetrize` is correct, it is sufficient to substitute polynomials for $s_1$ and
$s_2$, and expand the expression::

    >>> _[0].subs(_[2]).expand()
     2    2
    x  + y

Using the *slack variable* approach we can arrive with the same result using |groebner| bases. First
we need to construct non--trivial bivariate elementary symmetric polynomials. For this task we will
use :func:`symmetric_poly` function::

    >>> S1 = symmetric_poly(1, x, y)
    >>> S2 = symmetric_poly(2, x, y)

    >>> S1, S2
    (x + y, x⋅y)

Next we introduce two auxiliary (slack) variables $s_1$ and $s_2$ and compute a |groebner| basis of
$S_1 - s_1$ and $S_2 - s_2$ with respect to lexicographic ordering of monomials eliminating $x$ and $y$::

    >>> var('s1, s2')
    (s₁, s₂)

    >>> G = groebner([S1 - s1, S2 - s2], wrt=[x, y])

Finally we compute *symmetric reduction* of $x**2 + y**2$ by reducing this polynomial with respect to the
|groebner| basis $G$ eliminating variables $x$ and $y$::

    >>> reduced(x**2 + y**2, G, wrt=[x, y])[1]
      2
    s₁  - 2⋅s₂

We obtained the same result as with :func:`symmetrize`. Note, however, that :func:`symmetrize` implements
a specialized algorithm for computing symmetric reduction [PlanetMathSymmetric]_ and is much more efficient
than the general |groebner| bases approach. Lets now consider a polynomial $g = x^2 - y^2$. We will compute
symmetric reduction of $g$::

    >>> symmetrize(x**2 - y**2, formal=True)
    ⎛  2             2                      ⎞
    ⎝s₁  - 2⋅s₂, -2⋅y , {s₁: x + y, s₂: x⋅y}⎠

This time the remainder is non--zero, telling us that $g$ is not a symmetric polynomial. Nevertheless
:func:`symmetrize` expressed the symmetric part of $g$, not so surprisingly $x^2 + y^2$, in terms of
elementary symmetric polynomials, giving $-2 y^2$ as the remainder. As previously we can verify this
result::

    >>> _[0].subs(_[2]).expand() + _[1]
     2    2
    x  - y

Reusing the |groebner| basis $G$ lets compute symmetric reduction with :func:`reduced`::

    >>> reduced(x**2 - y**2, G, wrt=[x, y])[1]
      2
    s₁  - 2⋅s₁⋅y

In this case :func:`reduce` wasn't able to eliminate $y$ from its output, which tells us already
known fact that $x^2 - y^2$ isn't a symmetric polynomial. We can see the different between the
specialized symmetric reduction algorithm and the general algorithm, where the former one was
able to split the input polynomial into symmetric and non--symmetric parts and compute symmetric
reduction anyway.

Integer optimization
--------------------

Suppose we are in possession of American coins: pennies, nickels, dimes and quarters. We would like to
compose a certain quantity out of those coins, say 117, such that the *number* of coins used is *minimal*.
Lets forget about the minimality criterion for a moment. In this scenario it is not a big problem to
compose the requested value. We can simply take 117 pennies and we are done, as long as we have so
many of them. Alternatively we can take 10 dimes, 3 nickels and 2 pennies, or 2 quarters, 3 dimes,
5 nickels and 12 pennies, etc. There are quite a few combinations that can be generated to get the
desired value. But which of those combinations leads to the minimal number of necessary coins? To
answer this question we will take advantage of |groebner| bases computed with respect to a *total
degree* ordering of monomials [Buchberger2007talk]_.

First we should note that there are relations between values of particular coins, i.e. a nickel is
equivalent to 5 pennies, a dime has the same value as 10 pennies and a quarter consists of 25 pennies.
Those relations can be encoded as a system of polynomials. Lets introduce four variables $p$, $n$, $d$
and $q$, representing pennies, nickels, dimes and quarters respectively::

    >>> var('p, n, d, q')
    (p, n, d, q)

Now we write a system of polynomials representing relations between values of different coins::

    >>> F = [p**5 - n, p**10 - d, p**25 - q]

We encoded values of nickels, dimes and quarters in terms of pennies, by putting their values into
exponents of $p$ in consecutive polynomials. It would be perfectly valid to encode this in several
different ways, as long as we keep exponents as integers. As the next step we compute a |groebner|
bases of $F$ with respect to *graded lexicographic* (total degree) ordering of monomials::

    >>> G = groebner(F, order='grlex')

In previous examples we solved the given problems by elimination of variables, so we had to use
*lexicographic* ordering of monomials. This time our problem is a minimisation problem, so we take
advantage of *total degree* ordering. This is a correct choice because total degree ordering *takes*
monomials with smaller sums of exponents first and we can observe that the smaller the sum of exponents
in a solution to our coins problem will be, the less coins will be needed. So, the chosen ordering of
monomials encodes the cost function of our problem.

How to get the minimal number of required coins? Suppose we take any admissible solution to the studied
problem. This can be the trivial solution in which we take $117$ pennies or any other such that the
total value of coins is equal to $117$. We encode the chosen solution as a binomial with numbers of
particular coins as exponents of $p$, $n$, $d$ and $q$, and we reduce this binomial with respect to
the |groebner| basis $G$ utilizing, as previously, *graded lexicographic* ordering of monomials::

    >>> reduced(p**117, G, order='grlex')[1]
         2  4
    d⋅n⋅p ⋅q

The answer, that we were able to compute with |sympy|, is 4 quarters, 1 dime, 1 nickel and 2 pennies,
which altogether give the requested value of $117$. This is also the minimal solution to our problem.
We can try another admissible solution::

    >>> reduced(p**17*n**10*d**5, G, order='grlex')[1]
         2  4
    d⋅n⋅p ⋅q

but we will always arrive with the same minimal solution. This example might seem trivial, because we
can easily solve the problem by hand, however it shows the approach that can be further generalized for
solving arbitrary integer optimization problems (for a detailed theoretical and algorithmic background
see [Sturmfels1996lectures]_ and [Adams1994intro]_).

One should notice that the polynomials arising in this example are of a special, binomial form, where
there are few terms but very large exponents. |groebner| bases of systems of polynomials of this kind
are called toric |groebner| bases and there are modifications to the Buchberger algorithm, which can
make computations much more efficient in this special case [Traverso1991integer]_. Implementation of
algorithms for toric |groebner| bases is currently a work in progress in |sympy|.

This example showed us significance of other, than *pure lexicographic*, orderings of monomials. One
should note that in this particular case we were able to reuse *total degree* ordering. However, in
the general case of integer optimization, one has to invent a problem specific ordering with encodes
the cost function of the problem. This can be easily done in |sympy| by using ``key``--functions.

Coloring of graphs
------------------

Graph coloring, which is one of the oldest and best--known subfields of graph theory, is an
assigning values from a finite set, traditionally called colors, to elements (e.g. vertices,
edges) of a graph. The assignment is a subject to various constraints. Coloring of graphs is
a powerful technique for solving many practical discrete optimization problems, e.g. in
operational research, like scheduling, resource allocation and many other. Graph colorings
are also very interesting on their own due to their intrinsic complexity, as in the general
case (without any assumptions on the structure of the input graph) they are NP--hard problems,
i.e. there are no polynomial time algorithms for finding graph colorings (for a detailed
discussion on this subject refer to [Kubale2004color]_).

Classical vertex coloring
~~~~~~~~~~~~~~~~~~~~~~~~~

To show how |sympy| can be used for solving graph coloring problems using the |groebner|
bases method, lets focus on the classical problem of vertex coloring of graphs. We follow
[Adams1994intro]_ to give a brief theoretical introduction to this subject. Given a graph
$\mathcal{G}(V, E)$, where $V$ is the set of vertices of $\mathcal{G}$ and $E$ is the set
of edges of $\mathcal{G}$, and a positive integer $k$ we ask if is possible to assign a
color to every vertex from $V$, such that adjacent vertices have different colors assigned.
Moreover, we can extend our question and ask for all possible $k$--colorings of $\mathcal{G}$
or just for the number of $k$--colorings.

It shouldn't be that strange to use |groebner| bases for a graph theoretical problem. After
all, |groebner| bases have intrinsic complexity at least equal to the complexity of graph
coloring problems and allow analysis of the structure of studied problems.

But how do we transform a graph and coloring constraints into an algebraic problem? First we
need to assign a variable to each vertex. Given that $\mathcal{G}$ has $n$ vertices, i.e.
$|V| = n$, then we will have variables $x_1, x_2, \ldots, x_n$. Next we will write a set of
equations describing the fact that we allow an assignment of one of $k$ possible colors to every
vertex.  The currently best known approach to this problem is to map colors to primitive $k$--th
roots of unity. Let $\zeta = \exp(\frac{2\pi\I}{k})$ be a root of unity so that $\zeta^k = 1$. We
map colors $1, 2, \ldots, k$ to $k$ distinct roots of unity $1, \zeta, \ldots, \zeta^{k-1}$. As
$k$--th roots of unity are solutions to equation of the form $x_i^k - 1$ then the statement
that every vertex has to be assigned a color is equivalent to writing a set of polynomial
equations:

.. math::

    F_k = \{ x_i^k - 1 : i = 1, 2, \ldots, n \}

We also require that two adjacent vertices $x_i$ and $x_j$ are assigned different colors.
From the previous discussion we know that $x_i^k = 1$ and $x_j^k = 1$, so $x_i^k = x_j^k$
or, equivalently, $x_i^k - x_j^k = 0$. By factorization we can obtain that $x_i^k - x_j^k
= (x_i - x_j) \cdot f(x_i, x_j) = 0$. Since we require that $x_i \not= x_j$ then $x_i^k -
x_j^k$ can vanish only when $f(x_i, x_j) = 0$. This allows us to write another set of
polynomial equations:

.. math::

    F_{\mathcal{G}} = \{ f(x_i, x_j) : (i, j) \in E \}

We combine $F_k$ and $F_{\mathcal{G}}$ into one system of equations $F$. Let $\mathcal{I}$ be
the ideal of $\C\Xn$ generated by $F$ and let $\mathcal{V}(\mathcal{I})$ be an algebraic variety
in $\C^n$. Then a graph $\mathcal{G}$ is $k$--colorable if $\mathcal{V}(\mathcal{I}) \not= \emptyset$.
To verify this statement it is sufficient to compute a |groebner| basis $G$ of $F$ and check if
$G \not= \{1\}$. If this is the case, then the graph isn't $k$--colorable. Otherwise the |groebner|
basis gives us explicit information about all possible $k$--colorings of $\mathcal{G}$. Speaking in
less formal language, given a set of polynomial equations $F$ which describe geometry of a graph and
coloring constraints we look for solutions of this system of equations in $\C^n$. If we can find
solutions of any kind then the graph is colorable with $k$ colors.

Lets now focus on a particular and well known instance of $k$--coloring where $k = 3$. In this
case $F_3 = \{ x_i^3 - 1 : i = 1, \ldots, n \}$. Using |sympy|'s built--in multivariate polynomial
factorization routine::

    >>> var('x_i, x_j')
    (x_i, x_j)

    >>> factor(x_i**3 - x_j**3)
                ⎛   2                2⎞
    (x_i - x_j)⋅⎝x_i  + x_i⋅x_j + x_j ⎠

we derive the set of equations $F_{\mathcal{G}}$ describing an admissible $3$--coloring of a graph:

.. math::

    F_{\mathcal{G}} = \{ x_i^2 + x y + x_j^2 : (i, j) \in E \}

At this point it is sufficient to compute the |groebner| basis $G$ of $F = F_3 \cup F_{\mathcal{G}}$
to find out if a graph $\mathcal{G}$ is $3$--colorable, or not. After this theoretical introduction
lets consider a graph $\mathcal{G}(V, E)$ of figure :ref:`fig-graph-nocolor` with 12 vertices and
23 edges, to see that the described scheme works in practice. We ask if the graph is $3$--colorable.
In this example we will first show how to answer this question |sympy| and then we will compare this
with three other symbolic manipulation systems on the market: Maxima, Axiom and Mathematica.

.. tikz:: img/tikz/graph-nocolor.tex

.. _fig-graph-nocolor:
.. figure:: ../img/tikz/graph-nocolor.*
    :align: center

    The graph $\mathcal{G}(V, E)$.

The question, if $\mathcal{G}$ is $3$--colorable or not, is easy to answer by trial and error. We
are, however, an interested in algorithmic solution to the problem, so lets first encode $V$ and
$E$ of the graph $\mathcal{G}$ using Python's built--in data structures::

    >>> V = range(1, 12+1)
    >>> E = [(1,2),(2,3),(1,4),(1,6),(1,12),(2,5),(2,7),(3,8),
    ... (3,10),(4,11),(4,9),(5,6),(6,7),(7,8),(8,9),(9,10),
    ... (10,11),(11,12),(5,12),(5,9),(6,10),(7,11),(8,12)]

We encoded the set of vertices as a list of consecutive integers and the set of edges as a list
of tuples of adjacent vertex indices. Next we will transform the graph into an algebraic form by
mapping vertices to variables and tuples of indices into tuples of variables::

    >>> Vx = [ Symbol('x' + str(i)) for i in V ]
    >>> Ex = [ (Vx[i-1], Vx[j-1]) for i, j in E ]

As the last step of this construction we write equations for $F_3$ and $F_{\mathcal{G}}$::

    >>> F3 = [ x**3 - 1 for x in Vx ]
    >>> Fg = [ x**2 + x*y + y**2 for x, y in Ex ]

Everything is set following the theoretical introduction, so now we can compute the |groebner|
basis of $F_3 \cup F_{\mathcal{G}}$ with respect to *lexicographic* ordering of terms::

    >>> G = groebner(F3 + Fg, Vx)

We know that if the constructed system of polynomial equations has a solution then $G$ should be
non--trivial, i.e. $G \not= \emptyset$, which can be easily verified in |sympy|::

    >>> G != [1]
    True

The answer is that the graph $\mathcal{G}$ is colorable with $3$ colors. A sample coloring is shown
in figure :ref:`fig-graph-color`. Suppose we add an edge between vertices $i = 3$ and $j = 4$. Is
the new graph $3$--colorable? To check this it is sufficient to construct $F_{\mathcal{G'}}$ by
extending $F_{\mathcal{G}}$ with $x_3^2 + x_3 x_4 + x_4^2$ equation and recompute the |groebner|
basis::

    >>> x3, x4 = Vx[2], Vx[3]

    >>> G = groebner(F3 + Fg + [x3**2 + x3*x4 + x4**2], Vx)

    >>> G != [1]
    False

We got a trivial |groebner| basis as the result, so the graph $\mathcal{G'}$ isn't $3$--colorable. We
could continue this discussion asking if $\mathcal{G'}$ is $4$--colorable or if the number of colors
required to color the original graph could be lowered to $2$ colors.

.. tikz:: img/tikz/graph-color.tex

.. _fig-graph-color:
.. figure:: ../img/tikz/graph-color.*
    :align: center

    A sample $3$--coloring of the graph $\mathcal{G}(V, E)$.

Before we compare |sympy|'s syntax for computing |groebner| bases with other systems, let us clarify an
issue arising around list indexing (e.g. why we write ``x3 = Vx[2]``). |sympy| is a library built on top
of Python, so it utilizes Python's built--in data structures and their indexing schemes. Python, as a
general purpose programming language, uses well established zero--based indexing scheme, contrary to the
natural way of *indexing* things, i.e. saying 1st, 2nd, 3rd etc. (to which we are accustomed in real life
and mathematics). The zero--based indexing scheme dates back to the time of first programming languages,
which were hardware oriented (e.g. assemblers) and an index was understood as an offset from a particular
location in memory (the start of a container) to the requested item (for a more detailed discussion about
this issue see [Dijkstra1982zero]_). General purpose programming languages, even those interpreted like
Python, coherently follow this scheme. For |sympy|, this is a cost of building the system on top of a general
purpose language. As we will see in the following examples, other symbolic manipulation systems, i.e. those
which invent their own programming language, use *natural indexing* scheme. Currently a workaround to have
one--based indexing in |sympy|, is to append a dummy element in front of a list, e.g. to index ``Vx`` this
way we could issue ``Vx = [None] + Vx`` and then ``x3 = Vx[3]``.

Vertex coloring using other systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We showed so far how to solve classical vertex coloring problem with |sympy|. Lets now compare |sympy|'s
syntax and semantics of |groebner| bases functionality with three other mathematical software: Maxima,
Axiom and Mathematica.

One feature that makes |sympy| different from other mathematical systems is that |sympy| utilizes a general
purpose programming language for its core, modules and interaction with the user, whereas Maxima, Axiom
and Mathematica invent their own special languages for implementing their mathematical libraries and for
user interaction. This will require us to make some remarks also on the syntactic level.

Maxima, available at `<http://maxima.sourceforge.net>`_, implements |groebner| bases in an extension library.
Detailed documentation can be found in [MaximaGroebner]_. We will reuse the same example and, as much as
possible, the same computational approach. Maxima first requires us to load the |groebner| bases library.
Note that we write ``grobner`` in this case. User should also remember about putting a semicolon at the end
of every line. Next we define edges of the graph using a list of two element lists (there are no tuples in
Maxima).  Maxima uses very unusual syntax for variable assignment, utilizing colon for this purpose. In the
next step we define the list of variables ``Vx`` and systems of polynomial equations ``F3`` and ``Fg``.
Instead of list comprehensions we use :func:`makelist` function. One should note that Maxima uses ``^``
symbol for exponentiation, whereas Python uses this symbol for bitwise XOR operation. Finally we can compute
the |groebner| basis using :func:`poly_reduced_grobner`. Maxima by default assumes *lexicographic* ordering
of monomials. This information can be changed only by setting a global variable. As the last step we
check if the computed basis is non--trivial, utilizing :func:`is` and :func:`notequal` functions. Lets
see full source code for this example::

    (i1) load(grobner);

    (i2) E: [[1,2],[2,3],[1,4],[1,6],[1,12],[2,5],[2,7],[3,8],
    [3,10],[4,11],[4,9],[5,6],[6,7],[7,8],[8,9],[9,10],[10,11],
    [11,12],[5,12],[5,9],[6,10],[7,11],[8,12]];

    (i3) Vx: makelist(concat("x", i), i, 1, 12);

    (i4) F3: makelist(Vx[i]^3 - 1, i, 1, 12);
    (i5) Fg: [];

    (i6) for e in E do
            Fg: endcons(Vx[e[1]]^2 + Vx[e[1]]*Vx[e[2]] + Vx[e[2]]^2, Fg);

    (i7) G: poly_reduced_grobner(append(F3, Fg), Vx);

    (i8) is(notequal(G, [1]));
    (o8) true

Axiom, available at `<http://axiom-developer.org>`_, implements |groebner| bases toolkit in its
core algebra library. The documentation on this matter, thought not very extensive, can be found in
[Daly2003horizon]_. Axiom uses a sophisticated autoloader of its library components, so explicit package
loading in not necessary.  As previously we start with the definition of the set of edges using a list of
list. On should notice that, this time, the assignment operator is ``:=``. Semicolons at the end of lines
are not obligatory, however, useful for preventing printing of the results of computations. Next we define
``Vx`` and ``Ex`` in a way very similar to Python, as Axiom supports list comprehensions. The main difference
is Axiom's approach to indexing lists. Axiom does not use an object oriented language, as one might presume
looking at the source code, and it doesn't support properties. This give opportunity for reusing the dot
operator for indexing purpose (notice also one--base indexes). Next definitions of ``F3`` and ``Fg`` are
almost equivalent to what we wrote using |sympy|. Finally we compute the |groebner| basis using :func:`groebner`
function. Notice the ``::`` operator. It tells that the previously constructed polynomials should belong
to the domain that is on its right hand side, i.e. distributed multivariate polynomial in symbols from
``Vx`` with coefficients over integers. At the end we check that the basis in non--trivial using ``~=``
operator. Note that ``~=`` is not a comparison operator by default, but returns an unequality, so we
need to use coercion operator ``@`` to tell ``~=`` to end up with a ``Boolean`` result immediately.
Here is the full source code for this example::

    (1) -> E := [[1,2],[2,3],[1,4],[1,6],[1,12],[2,5],[2,7],
    [3,8],[3,10],[4,11],[4,9],[5,6],[6,7],[7,8],[8,9],[9,10],
    [10,11],[11,12],[5,12],[5,9],[6,10],[7,11],[8,12]];

    (2) -> Vx := [ concat("x", i::String)::Symbol for i in 1..12 ];
    (3) -> Ex := [ [Vx.(e.1), Vx.(e.2)] for e in E ];

    (4) -> F3 := [ x**3 - 1 for x in Vx ];
    (5) -> Fg := [ e.1**2 + e.1*e.2 + e.2**2 for e in Ex];

    (6) -> G := groebner([ f::DMP(Vx, INT) for f in concat(F3, Fg) ]);

    (7) -> (G ~= [1]) @ Boolean
       (7) true

Mathematica, available at `<http://www.wolfram.com/mathematica/>`_, has extensive built--in support
for |groebner| bases. Detailed documentation on this matter can be found in [MathematicaGroebner]_.
Mathematica has a very peculiar language for interaction with the user and its syntax, which was
influence by the infix dialect of lisp (or m--lisp), is very different from other languages used
in symbolic mathematics, so will skip detailed syntactic comparison and refer the reader to
[Wolfram2003book]_.

::

    In[1]:= Unprotect[E];
    In[2]:= E := {{1,2},{2,3},{1,4},{1,6},{1,12},{2,5},{2,7},
    {3,8},{3,10},{4,11},{4,9},{5,6},{6,7},{7,8},{8,9},{9,10},
    {10,11},{11,12},{5,12},{5,9},{6,10},{7,11},{8,12}}

    In[3]:= Vx := Table[Symbol["x" <> ToString[i]], {i,1,12}]
    In[4]:= h[{i_, j_}] := Vx[[i]]^2 + Vx[[i]] Vx[[j]] + Vx[[j]]^2

    In[5]:= F3 := Map[(#^3-1)&, Vx]
    In[6]:= Fg := Map[h, E]

    In[7]:= G := GroebnerBasis[Join[F3, Fg], Vx]

    In[8]:= G != {1}
    Out[8]= True

We showed how to perform classical vertex coloring of a graph based on the |groebner| bases method
using |sympy| and three other mathematical systems. It is interesting to compare the times that were
needed to compute the |groebner| basis $G$ by each of those systems. Timings (average of multiple
runs) were collected in figure :ref:`fig-groebner-time-compare`. This simple study shows that both
|sympy| and Maxima are significantly slower than Axiom and Mathematica. This happens, because the
implementation of |groebner| bases in both systems is done in an interpreted language (Python and
Maxima language, respectively). Possibly they also implement less(--powerful) criteria for eliminating
useless critical pairs.

.. _fig-groebner-time-compare:
.. figure:: ../img/plot/groebner-time-compare.*
    :align: center

    Average timing for computing |groebner| basis of graph $\mathcal{G}(V, E)$.

..
    +----------+-------+--------+-------+-------------+
    |          | SymPy | Maxima | Axiom | Mathematica |
    +==========+=======+========+=======+=============+
    | Time [s] | 15.4  | 17.6   | 3.6   | 0.34        |
    +----------+-------+--------+-------+-------------+

The structure of vertex coloring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Till this point we showed how to check with |sympy| that a graph is $k$--colorable or not. However, using
the |groebner| bases method, we can obtain a much more exciting result. Suppose that $G$ is a lexicographic
|groebner| basis of a system of polynomials $F$ describing a vertex $k$--coloring problem. To prove
that a graph is $k$--colorable we used the fact that $G \not= \{1\}$. We know that $G$ and $F$ have
the same set of solutions, however, $G$ has more structure than $F$. We can take advantage of this
and find all possible $k$--colorings of a graph by solving $G$ over the complex field.

Lets first revise our approach to vertex coloring. To transform a graph problem in a polynomial problem,
we mapped colors to primitive roots of unity. In our example of $3$--coloring, the three colors were, say
red, green and blue, were mapped to $1$, $\zeta$, $\zeta^2$, where $\zeta = \exp(\frac{2\pi\I}{k})$. In
other words we worked in a field generated by $\zeta$::

    >>> zeta = exp(2*pi*I/3).expand(complex=True)

    >>> zeta
        ___
    I⋅╲╱ 3
    ─────── - 1/2
       2

Thus to tell that every vertex should be assigned a color we wrote a system of equations of the form
$x_i^3 - 1$, where $i \in \{1, \ldots, |V|\}$. Lets factor this polynomial over $\Q[\zeta]$::

    >>> factor(x**3 - 1, extension=zeta)
            ⎛        ___      ⎞ ⎛        ___      ⎞
            ⎜    I⋅╲╱ 3       ⎟ ⎜    I⋅╲╱ 3       ⎟
    (x - 1)⋅⎜x + ─────── + 1/2⎟⋅⎜x - ─────── + 1/2⎟
            ⎝       2         ⎠ ⎝       2         ⎠

We obtained the splitting factorization of $x_i^3 - 1$ and we can clearly see how our mapping works.
Lets now solve each of the above linear obtaining a list of primitive roots of unity of order three::

    >>> [ solve(arg)[0] for arg in _.args ]
    ⎡         ___            ___      ⎤
    ⎢     I⋅╲╱ 3         I⋅╲╱ 3       ⎥
    ⎢1, - ─────── - 1/2, ─────── - 1/2⎥
    ⎣        2              2         ⎦

Going one step ahead, lets declare three variables which will literally represent colors in the studied
$3$--coloring problem and lets put together, in an arbitrary but fixed order, those variables and the
previously computed roots of unity::

    >>> var('red,green,blue')
    (red, green, blue)

    >>> colors = zip(__, _)

    >>> colors
    ⎡          ⎛      ___             ⎞  ⎛    ___            ⎞⎤
    ⎢          ⎜  I⋅╲╱ 3              ⎟  ⎜I⋅╲╱ 3             ⎟⎥
    ⎢(1, red), ⎜- ─────── - 1/2, green⎟, ⎜─────── - 1/2, blue⎟⎥
    ⎣          ⎝     2                ⎠  ⎝   2               ⎠⎦

Now we are prepared to study the structure of the |groebner| basis $G$. To make the analysis easier, we
we will split $G$ into groups, discriminating polynomials by their degree and their number of terms::

    >>> key = lambda f: (degree(f), len(f.args))
    >>> groups = split(G, key, reverse=True)

    >>> len(groups)
    4

We obtained four groups of polynomials, so lets analyzed them one--by--one::

    >>> groups[0]
    ⎡   3    ⎤
    ⎣x₁₂  - 1⎦

In the first group we have just a single polynomial of the well known form. This tells us that $x_{12}$
can be assigned any of the three possible colors. This wasn't very interesting, so lets move the next
group::

    >>> groups[1]
    ⎡   2                2⎤
    ⎣x₁₁  + x₁₁⋅x₁₂ + x₁₂ ⎦

From the construction of the system of polynomials $F_{\mathcal{G}}$, which describes an admissible
vertex coloring for the graph $\mathcal{G}$, we know that the above equation is zero when $x_{11}$
is different from $x_{12}$. Still we didn't learn anything new, so lets move to the third group::

    >>> groups[2]
    [x₁ + x₁₁ + x₁₂, x₁₁ + x₁₂ + x₅, x₁₁ + x₁₂ + x₈, x₁₀ + x₁₁ + x₁₂]

This time we got a lot more polynomials, which are of a new form. We should recall that we use
primitive roots of unity for color assignment. Roots of this kind have the property that their
sum is zero. So, from the above equations we can read that triples of vertices $x_i$, $x_{11}$
and $x_{12}$, where $i \in \{1, 5, 8, 10\}$, should be assigned different colors. This is a
piece of knowledge that we didn't see in $F$ but we were able to learn from $G$. Lets move
to the last group::

    >>> groups[3]
    [-x₁₁ + x₂, -x₁₂ + x₃, -x₁₂ + x₄, -x₁₁ + x₆, -x₁₂ + x₇, -x₁₁ + x₉]

In the last group we got a set of trivial equations of the form $x_i = x_j$, which tell us that
particular pairs of vertices should have the same color assigned. What we described here is a
complete knowledge necessary to invent a $3$--coloring for $\mathcal{G}$.

Following this analysis of the structure of the |groebner| basis $G$, to find a $3$--coloring of
the graph $\mathcal{G}$, first we need to choose a color for $x_{12}$. Suppose we let $x_{12}$ to
have red color assigned. Then we have to assign a color other than red to $x_{11}$. Let it be green.
From the fourth group of equations from $G$ we know that $x_3$, $x_4$ and $x_7$ will be assigned the
same color as $x_{12}$, i.e. red, and $x_2$, $x_6$ and $x_9$ will have the same color as $x_{11}$,
i.e. blue. Then it is sufficient to assign other vertices, mainly $x_1$, $x_5$, $x_8$ and $x_{10}$,
with green color. This way we obtained a single admissible $3$--coloring of the graph $\mathcal{G}$
(the same as the coloring of figure :ref:`fig-graph-color`).

What about other admissible $3$--colorings? We can continue with the above procedure and generate
more colorings. It would be, however, more interesting if we could get all solutions to our graph
problem at once. To do this with |sympy|, we will simply solve $G$::

    >>> colorings = solve(G, Vx)

    >>> len(colorings)
    6

We got six admissible $3$--colorings for $\mathcal{G}$. This is correct because there are three ways
to assign $x_{12}$ a color, then there are only two ways to assign $x_{11}$ a color for each possible
coloring of $x_{12}$, and, with colors assigned to $x_{11}$ and $x_{12}$, there is only one way to
assign colors to other vertices.

At this point we could simply print the computed solutions to see what are the admissible $3$--colorings.
This is, however, not a good idea, because we use algebraic numbers (roots of unity) for representing colors
and :func:`solve` returned solutions in terms of those algebraic number, possibly even in a non--simplified
form. To overcome this difficulty we will use previously defined mapping between roots of unity and literal
colors::

    >>> for coloring in colorings:
    ...     print [ elt.expand(complex=True).subs(colors) for elt in coloring ]
    ...
    ...
    [blue, green, red, red, blue, green, red, blue, green, blue, green, red]
    [green, blue, red, red, green, blue, red, green, blue, green, blue, red]
    [green, red, blue, blue, green, red, blue, green, red, green, red, blue]
    [red, green, blue, blue, red, green, blue, red, green, red, green, blue]
    [blue, red, green, green, blue, red, green, blue, red, blue, red, green]
    [red, blue, green, green, red, blue, green, red, blue, red, blue, green]

This is the result we were looking for, but a few words of explanation are needed. As :func:`solve` may
return unsimplified results, we need to simplify any algebraic numbers that don't match structurally with
the precomputed roots of unity. Taking advantage of the domain of computation, we use complex expansion
algorithm for this purpose. Having the solutions in a normal form, to get this nice form with literal
colors it is sufficient to substitute *color* variables for roots of unity.

There is one more important thing, which we must emphasise. When solving the |groebner| basis $G$, we
specified the list of symbols explicitly using ``Vx``. In general this is unnecessary and :func:`solve`
can work perfectly without this knowledge. However, in our case this additional piece of information
was significant, because it guaranteed proper order of color assignments in the solution. Most functions
in |sympy| can derive variables of the problem being solved on their own, but in complex situations this
may lead to wrong results or at least can complicate analysis of solutions. If unsure what a particular
function will do, always specify variables explicitly.

Algebraic geometry
------------------

Geometry is one of the primary subjects taught during elementary mathematics classes and using |sympy| for
studying theorems of Euclidean geometry seems a very promising idea. For example, lets consider a rhombus
(in a fixed coordinate system). We would like to prove a theorem that diagonals of a rhombus are mutually
perpendicular. We are of course interested in a purely algorithmic approach to solve this problem. To prove
this theorem we will use the machinery of |groebner| bases.

Following [Winkler1990geometry]_, lets consider a geometric entity which properties can be translated into a
system of $m$ polynomials, say $\mathcal{H} = \{f_1, \ldots, f_m\}$. We will call $\mathcal{H}$ a hypothesis.
Given a theorem concerning this geometric entity, the algebraic formulation is as follows:

.. math::

    \forall_{x_1, \ldots, x_n, y_1, \ldots, y_n} (f_1 = 0 \vee \ldots \vee f_m = 0) \Rightarrow g = 0

where $g$ is the conclusion of the theorem and $f_1, \ldots f_m$ and $g$ are polynomials in $\K[x_1, \ldots,
x_n, y_1, \ldots, y_n]$. It follows from the |groebner| bases theory that the above statement is true when $g$
belongs to the ideal generated by $\mathcal{H}$. To check this, i.e. to prove the theorem, it is sufficient
to compute |groebner| basis of $\mathcal{H}$ and reduce $g$ with respect to this basis. If the theorem is
true then the remainder from the reduction will vanish. In this example, for the sake of simplicity, we
assume that the geometric entity is non--degenerate, i.e. it does not collapse into a line or a point.
Anyway, the |groebner| basis approach allows to prove theorems in algebraic geometry in full generality
and derive automatically non--degeneracy conditions.

.. tikz:: img/tikz/geometry-rhombus.tex

.. _fig-geometry-rhombus:
.. figure:: ../img/tikz/geometry-rhombus.*
    :align: center

    A rhombus in a fixed coordinate system.

Lets consider the rhombus of figure :ref:`fig-geometry-rhombus`. This geometric entity consists of four
points $A$, $B$, $C$ and $D$. To setup a fixed coordinate system, without loss of generality, we can
assume that $A = (0, 0)$, $B = (x_B, 0)$, $C = (x_C, y_C)$ and $D = (x_D, y_D)$. This is possible by
taking rotational invariance of the geometric entity. We will prove that the diagonals of this rhombus,
i.e. $AD$ and $BC$ are mutually perpendicular. We have the following conditions describing $ABCD$:

#. Line $AD$ is parallel to $BC$, i.e. $AD \parallel BC$.
#. Sides of $ABCD$ are of the equal length, i.e. $AB = BC$.
#. The rhombus is non--degenerate, i.e. is not a line or a point.

Our conclusion is that $AC \bot BD$. To prove this theorem, first we need to transform the above conditions
and the conclusion into a set of polynomials. How we can achieve this? Lets focus on the first condition. In
general, we are given two lines $A_1A_2$ and $B_1B_2$. To express the relation between those two lines, i.e.
that $A_1A_2$ is parallel $B_1B_2$, we can relate slopes of those lines:

.. math::

    \frac{y_{A_2} - y_{A_1}}{x_{A_2} - x_{A_1}} = \frac{y_{B_2} - y_{B_1}}{x_{B_2} - x_{B_1}}

Clearing denominators in the above expression and putting all terms on the left hand side of the equation, we
derive a general polynomial describing the first condition. This can be literally translated into Python::

    def parallel(A1, A2, B1, B2):
        """Line [A1, A2] is parallel to line [B1, B2]. """
        return (A2.y - A1.y)*(B2.x - B1.x) - (B2.y - B1.y)*(A2.x - A1.x)

assuming that ``A1``, ``A2``, ``B1`` and ``B2`` are instances of :class:`Point` class. In the case of our
rhombus, we will take advantage of the fixed coordinate system and simplify the resulting polynomials as
much as possible. The same approach can be used to derive polynomial representation for other conditions
and the conclusion. To construct $\mathcal{H}$ and $g$ we will use the following functions::

    def distance(A1, A2):
        """The squared distance between points A1 and A2. """
        return (A2.x - A1.x)**2 + (A2.y - A1.y)**2

    def equal(A1, A2, B1, B2):
        """Lines [A1, A2] and [B1, B2] are of the same width. """
        return distance(A1, A2) - distance(B1, B2)

    def perpendicular(A1, A2, B1, B2):
        """Line [A1, A2] is perpendicular to line [B1, B2]. """
        return (A2.x - A1.x)*(B2.x - B1.x) + (A2.y - A1.y)*(B2.y - B1.y)

The non--degeneracy statement requires a few words of comment. Many theorems in geometry are true only
in the non--degenerative case and false or undefined otherwise. In our approach to theorem proving in
algebraic geometry, we must supply sufficient non--degeneracy conditions manually. In the case of our
rhombus this is $x_B > 0$ and $y_C > 0$ (we don't need to take $x_C$ into account because $AB = BC$).
At first, this seems to be a show stopper, as |groebner| bases don't support inequalities. However,
we can use Rabinovich trick and transform those inequalities into a single polynomial condition by
introducing an additional variable, say $a$, about which we will assume that is positive. This gives
us a non--degeneracy condition $x_B y_C - a$.

With all this knowledge we are ready to prove the main theorem. First, lets declare variables::

    >>> var('x_B, x_C, y_C, x_D, a')
    (x_B, x_C, y_C, x_D, a)

    >>> vars = _[:-1]

We had to declare the additional variable $a$, but we don't consider it a variable of our problem. This
will lead to a new case in |sympy|'s implementation of |groebner| bases, because we will be computing not
over rationals, as we did in all previous examples, but the computations will be done over the field of
univariate rational functions. Lets now define the four points $A$, $B$, $C$ and $D$::

    >>> A = Point(0, 0)
    >>> B = Point(x_B, 0)
    >>> C = Point(x_C, y_C)
    >>> D = Point(x_D, y_C)

Using the previously defined functions we can define the hypothesis::

    >>> h1 = parallel(A, D, B, C)
    >>> h2 = equal(A, B, B, C)
    >>> h3 = x_B*y_C - a

and compute its |groebner| basis::

    >>> G = groebner([h1, h2, h3], vars, order='grlex')

Two things need a comment here. Previously we specified variables in :func:`groebner`, when we were
concerned about the order of variables. This was necessary when the task was to eliminate particular
variables, before proceeding to the other steps of an algorithm. However, in this case we are rather
concerned about not letting the variable $a$ to be considered as a significant variable in the problem,
because we treat $a$ as a parameter. The other thing is that we can compute the |groebner| basis with
respect to any admissible ordering of monomials. We chose the standard total degree scheme, over the
default lexicographic ordering, because leads to shorter computation times.

Lets now verify the theorem::

    >>> reduced(perpendicular(A, C, B, D), G, vars, order='grlex')[1]
    0

This proves that $AC \bot BD$. Although, the theorem we described and proved was a simple one, one can
handle much more complicated problems as well. One should refer to Winkler's paper for more interesting
examples, especially concerning issues with degenerate cases.

Other applications
------------------

So far several detailed examples of practical applications of the |groebner| bases method were
presented, which explained most interesting features of |groebner| bases and their use patterns
in |sympy|. Following the list from the beginning of this section, there are, however, many more
applications. We will give reference to several of them in this part.

Besides the obvious application of solving systems of polynomial equations and the less obvious
for computing LCMs and GCDs of multivariate polynomials, the |groebner| basis method is also used
in |sympy| for computing minimal polynomials of algebraic numbers, primitive elements of algebraic
fields and isomorphisms between algebraic fields (for a detailed theoretical discussion see
[Adams1994intro]_ and algorithms refer to [Cohen1993course]_). For all those tasks there
are much more efficient algorithms implemented in |sympy|. However, |groebner| bases remain the
fallback tool if any of the fast algorithms isn't suitable for a particular job. For example,
minimal polynomials can be relatively easily computed using PSLQ algorithm (see :func:`pslq`
function in mpmath library) but only in the case of real algebraic numbers. In the more general
case of complex algebraic numbers the |groebner| bases method is the only choice.

|groebner| bases can be also directly applicable in symbolic manipulation systems for computing
factorizations of multivariate polynomials [Gianni1985groebner]_ or evaluating symbolic summations
and integrals [Chyzak1998groebner]_.

Complexity of computing |groebner| bases
========================================

Depending on our point of view, the complexity of the |groebner| bases method may vary. |groebner|
bases can be considered easy when we are discussing the general idea that stands behind them, or
the structure of Buchberger algorithm. As we saw in section :ref:`gb-construct`, the operations
needed to compute a |groebner| basis are elementary and taught in high--school, and it shouldn't be
very difficult, for a high--school student, to experiment with |groebner| bases, especially in Python.

However, the algorithmic complexity of the |groebner| basis method is very high. This is not a
surprise, as in the examples we were able to solve several problems which intrinsic complexity
is exponential. Thus, in the general setup, the Buchberger has exponential complexity as well,
whereas in *pathological* cases its complexity may increase to doubly exponential. It should be
emphasised that the Buchberger algorithm is very fragile to the choice of the ordering of
monomials, so it often happens that a |groebner| basis, for a set of polynomials, with respect
to one ordering is computable in relatively short time, whereas to compute it with respect to
another ordering one would have to wait ages. Lexicographic |groebner| bases are considered to
be the most expensive ones. In [Buchberger2001systems]_ we can find a simple--looking system
of three polynomials in three variables:

.. math::

    \left\{
    \begin{array}{l}
        x y^3 - 2 y z - z^2 + 13          \\
        y^2 - x^2 z + x z^2 + 3           \\
        z^2 x - y^2 x^2 + x y + y^3 + 12
    \end{array}
    \right.

for which a |groebner| basis with respect to lexicographic ordering can't be computed in a *reasonable*
time in |sympy|. However, if we switch to graded lexicographic ordering of monomials, |sympy| requires
less than a second to construct the basis. For comparison, Mathematica can compute both bases at glance
(refer to [MathematicaInternal]_ for a description of its implementation of Buchberger algorithm).

However, as the examples showed us, there is often a lot of *structure* in the |groebner| bases found
in practical applications, so many non--trivial and interesting |groebner| bases are relatively simple
to compute.

There many improvements possible to the |sympy|'s implementation of Buchberger algorithm. Techniques like
|groebner| Walk, which allows to compute a basis with respect to a *cheaper* ordering of monomials first
and then convert it to a more expensive one, or linear algebra approach [Faugere1999f4]_, in which a
polynomial algebra problem is transformed in into a linear algebra problem and solved using efficient
algorithms available in this field, are all applicable in |sympy|. Ideas for improving the |groebner|
bases module are listed, among other, as *Google Summer of Code* proposals at [SymPyGSoC2010]_.

Currently the most promising approach for improving the Buchberger algorithm is |sympy|, which is scheduled
for implementation in near future, is algorithm F5 due to Jean Charles Faugère (see [Faugere2002f5]_ and
[Stegers2006f5]_). The algorithm has the same structure as Buchberger algorithm, however it utilizes a very
powerful criteria for elimination of useless critical pairs, significantly reducing the number of required
polynomial divisions.  In practical cases there are *no* reductions to zero in F5 algorithm. Reductions to
zero may happen in certain situations, however, their number is still less than in any other algorithm for
computing |groebner| bases. Thus F5 is considered to be at least one order of magnitude faster than the
fastest algorithm previously available.

Conclusions
===========

The |groebner| bases method is a powerful tool in symbolic and algebraic computing, which is currently
not yet fully utilized in |sympy|. Also implementation of Buchberger's algorithm is quite limited at
the moment. However, as we showed in this chapter, |sympy| can be used for solving practical problems
in symbolic mathematics, specifically problems which involve solving systems of polynomials. We hope
that, in foreseeable future, improved algorithms for computing |groebner| bases will be implemented,
so that |sympy| will be able to tackle more complex problems.

