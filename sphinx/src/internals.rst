.. include:: ../globals.def

.. _thesis-internals:

====================================
Notes on the internal implementation
====================================

Knowing the goals of the project, lets now focus on the internal implementation of polynomials
manipulation module and methods that were used to reach the goals. In this chapter we will describe
step--by--step all details concerning the design and implementation of the module, from the technical
point of view. In the next chapter we will jump in the details of implemented algorithms.

Physical structure of the module
================================

Polynomials manipulation module consists of a single, ``sympy/polys``,  directory with Python source
files:

``sympy/polys/__init__.py``
    Contains imports of the public API.

``sympy/polys/algebratools.py``
    Definitions of categories and domains.

``sympy/polys/densearith.py``
    Arithmetics algorithms for dense polynomial representation.

``sympy/polys/densebasic.py``
    Basic (e.g. conversion) algorithms for dense polynomial representation.

``sympy/polys/densetools.py``
    Advanced (e.g. GCD, SQF) algorithms for dense polynomial representation.

``sympy/polys/factortools.py``
    Low--level algorithms for polynomial factorization.

``sympy/polys/galoistools.py``
    Implementation of efficient univariate polynomials over finite fields.

``sympy/polys/groebnertools.py``
    Sparse distributed polynomials and |groebner| bases (Buchberger) algorithm.

``sympy/polys/monomialtools.py``
    Functions and classes for enumerating and manipulating monomials.

``sympy/polys/numberfields.py``
    Tools for computations in algebraic number fields.

``sympy/polys/orthopolys.py``
    Functions for generating orthogonal polynomials.

``sympy/polys/polyclasses.py``
    OO layer over low--level polynomial manipulation functions.

``sympy/polys/polyconfig.py``
    Tools for configuring functionality of the module.

``sympy/polys/polycontext.py``
    Tools for managing contexts of evaluation.

``sympy/polys/polyerrors.py``
    Definitions of polynomial specific exceptions.

``sympy/polys/polyoptions.py``
    Managers of options that can used with the public API.

``sympy/polys/polyroots.py``
    Algorithms for root finding, specifically via radicals.

``sympy/polys/polytools.py``
    The main part of the public API of polynomials manipulation module.

``sympy/polys/polyutils.py``
    Internal utilities for expression parsing, handling generators etc.

``sympy/polys/rootisolation.py``
    Low--level algorithms for symbolic real and complex root isolation.

``sympy/polys/rootoftools.py``
    Tools for formal handling of polynomial roots: ``RootOf`` and ``RootSum``.

``sympy/polys/specialpolys.py``
    A collection of functions for generating special sorts of polynomials.

There are also two subdirectories with tests and benchmarks. Altogether there are about 1900
functions and methods, and about 90 classes in about 30 thousandth lines of code. We don not
give exact measures because those statistics are not that important and are changing all the
time.

Logical structure of the module
===============================

One of the main concerns when designing a symbolic manipulation library, especially one which is
written in an interpreted general purpose programming language, is speed. Even the best equipped
library, with most recent, cutting edge algorithms and data structures, user friendly API and
easily configurable internals, has little value if the user needs to wait ages for any, even
trivial, results. This was recently the main problem with |sympy| in general and its fundamental
weakness. It should be clearly understood that code written in an interpreted language will be
always slower than compiled code, unless we had a very clever JIT (Just--In--Time) compiler which
could optimize and compile the code on--the--fly. There is some progress in this area, especially
within projects Unladen Swallow [UnladenSwallow]_ and PyPy [PyPy]_, but we are still waiting for
truly working solutions. This, however, should not be discouraging and we are supposed to put our
best efforts to make |sympy| as fast as possible on pure Python level, especially when implementing
the infrastructure which is used everywhere else in the library.

There is a trivial observation about interpreted programming languages: there is a very high cost
associated with every function call and with every use of *magic* functionality of the language of
choice. This statement is true in the general case of interpreted languages and the first part is
especially true in the case of Python programming language. There is another observation concerning
algorithms of symbolic mathematics: often they require very large number of function calls. The number
varies between different algorithms, but for the most complex ones, the number can be as high as millions
(or more) function calls per algorithm execution.

One obvious (in theory) solution to this problem is to use *better* algorithms. Unfortunately, it
is not clear what we mean by better in this context. If we take only pure algorithmic complexity
of methods we implement in |sympy|, then one could argue that we should always implement polynomial
time algorithms, of course if they exist in the particular area of interest. This would be a perfect
solution, however, an interesting phenomenon occurs. Often polynomial time algorithms are slower for
common input than their counter parts which exhibit exponential time complexity. This is true, for
example, in the case of polynomial factorization algorithms, where LLL algorithm [Lenstra1982factor]_,
the only known polynomial time approach to polynomial factorization, is almost always slower than
*efficient* exponential time algorithms. Besides this phenomenon, whatever approach we take for choosing
a good algorithm for implementation in |sympy| for improving speed, there is always a high cost associated
with such development, because first one has to assure correctness of the newly implemented algorithm and
only then think about improving speed. Of course, this is what we do in |sympy| and a discussion about
algorithms will follow in the next chapter.

There is, however, another method for significantly improving computations speed. In parallel with
implementation of *better* algorithms, one can eliminate as much overhead as possible. The overhead
is associated with the cost of interpretation of program code. As we stated before, the cost of
function calls in Python is high and the more *advanced* constructs of the language we use the
higher the cost is. However, the less *magic* we use the harder is to use the code, so our task
is to find the cross--over point, where we have balance between speed and usability. This is
because speed without usability is as much pointless as usability without speed.

The answer to those observations is a design of polynomials manipulation module in a form of a
multiple--level environment, where on the lowest level are fundamental functions which are run
most often and form a computational basis for other levels which tend to be much more oriented
towards the user, adding the cost associated with more user friendly API. Multiple--levels is
nothing new to symbolic mathematics and this is how things were done from the very beginning.
However, previously those levels were associated with usage of different programming languages,
where the core was one level, written in a compiled programming language like C or C++, and
usually not accessible by the end user. The other was a library of mathematical algorithms,
written in a domain specific language (DSL), designed specially for a particular symbolic
mathematics system. Contrary, |sympy| is written entirely in a single, interpreted programming
language, so we introduce multiple levels in this language by selecting appropriate sets of
feasible features of the language for each level.

In polynomials manipulation module four levels were introduced: L0, L1, L2 and L3. Each level
has its own syntax and API, and is used for different tasks in |sympy|. Redundancy between
levels is reduced to minimum, so that not a single algorithm is duplicated on any level. Also
tests were designed the way that they only test correctness of incrementally added functionality.
On the lowest level we test correctness of the implementations of algorithms of mathematics, and
on other levels we test (mostly) APIs and correctness of argument passing. The first two levels,
L0 and L1, are used internally in the module. The other two levels form the public API of the
module and are used extensively in other parts of |sympy| and in interactive sessions.

Motivation
----------

Why we need exactly four levels in polynomials manipulation module? Suppose we need to compute
a factorization of polynomial $x^{10} - 1$. There are four levels, so we can perform the same
computation in four different ways::

    >>> f3 = x**10 - 1
    >>> %timeit factor_list(f3)
    100 loops, best of 3: 5.57 ms per loop

    >>> f2 = Poly(x**10 - 1, x, domain='ZZ')
    >>> %timeit f2.factor_list()
    100 loops, best of 3: 2.15 ms per loop

    >>> f1 = DMP([mpz(1), mpz(0), mpz(0), mpz(0), mpz(0),
    ... mpz(0), mpz(0), mpz(0), mpz(0), mpz(0), mpz(-1)], ZZ)
    >>> %timeit f1.factor_list()
    100 loops, best of 3: 1.90 ms per loop

    >>> f0 = [mpz(1), mpz(0), mpz(0), mpz(0), mpz(0),
    ... mpz(0), mpz(0), mpz(0), mpz(0), mpz(0), mpz(-1)]
    >>> %timeit dup_factor_list(f0, ZZ)
    100 loops, best of 3: 1.88 ms per loop

We factored polynomial $x^{10} - 1$ starting with the highest level and ending on the lowest
level. On L3 we used an expression to construct the polynomial and we did not have to pay any
attention to the details, which were figured out automatically by :func:`factor_list` function.
On L2 we created a polynomial explicitly by providing a generator and coefficient domain. This
time we used :func:`factor_list` method of :class:`Poly`. This computation took less than half
of time that was needed to compute the same thing on L3. Next we performed the same computation
on L1 level, the first internal level of the module, constructing the polynomial by providing
an explicit polynomial representation (dense in this case) and we gained a 10% speedup. Finally
we computed the factorization on the lowest level, gaining tiny speed improvement.

We can see that, depending on the level on which we performed the computation, we had to pay
increasingly more attention to the technical details, but we gained speed improvement thanks
to this. The improvement might not seem very encouraging, especially when we compare levels
L2, L1 and L0. However, we have to keep in mind that those milli-- or microseconds that we
save with each computation, have to be multiplied by the number of all computations we do,
and from this perspective we do not save only fractions of seconds but we save seconds or
even minutes or hours of computation time.

The zeroth level: L0
--------------------

This is the lowest level of polynomials manipulation functionality, which is used only for internal
purpose of the module. Most algorithms that the module implements, especially those which are most
commonly used as parts of other algorithms or are most computationally demanding, are implemented
on this level. This includes algorithms for polynomial arithmetics, GCD and LCM computation,
square--free decomposition, polynomial factorization, root isolation, |groebner| bases and others.

To reduce the overhead of Python to minimum, the zeroth level is implemented in purely procedural
style: it consists only of functions and all data is passed explicitly via arguments to functions.
On this level we do not take advantage of any runtime magic like context managers, everything is
done explicitly. Besides being fast, this has also the benefit that the code is very verbose and
thus easily understandable, which is not often the case in object--oriented programming. It might
seem a bit awkward, after so many years of declining of procedural programming, to use this old
fashioned style, but currently it seems the right choice. Although, in the opinion of the author,
procedural code is easy to understand, it is not that easy to write, especially for newcomers,
because of very high level of verboseness of such code. However, this is the trade--off we have
to make, to make |sympy| both usable and reasonably fast.

Functions on this level are spread over several source files in ``sympy/polys`` and are split into
groups, depending on which polynomial representation they belong to and what kind of ground domain
can be used with them. Currently there are four major groups, which can be distinguished by their
special prefixes:

* ``gf_`` --- dense univariate polynomials over finite (Galois) fields

* ``dup_`` --- dense univariate polynomials over arbitrary domains

* ``dmp_`` --- dense multivariate polynomials over arbitrary domains

* ``sdp_`` --- sparse distributed polynomials over arbitrary domains

There are additional minor suffixes, which can be added to the major prefixes. They are used to tell
the difference between the same function, e.g. for computing the greatest common divisor, for various
ground domains. The typically used suffixes are ``zz_``, ``qq_``, ``rr_`` and ``ff_``, which stand
for the ring of integers, the rational field, a ring and a field, respectively. Note that those
suffixes are not combined with the ``gf_`` prefix, which already limits the possible ground domains
to a single one. Usually, if a function comes with a suffix, then it will be defined for both, either
``zz_`` and ``qq_``, or ``rr_`` and ``ff_`` suffixes. There will be also a function without any suffix,
which will dispatch the flow to an appropriate function for a specialized ground domain, depending on
the analysis of the ground domain argument to this function. This separation is necessary, because it
often happens that functions for computing a particular thing over different ground domains, have very
different semantics and internal structure. A good examples are functions for computing GCDs and
factorizations of polynomials. One should also note that even if there is a separation between different
ground domains, it is still possible (and it often happens) that a function for a more general domain
will transform the problem and run an algorithm for a smaller domain, to take advantage of more efficient
algorithms.

Although we listed four groups of types of functions, there are really only three true groups, because
``dup_`` and ``dmp_`` depend on each other, forming a larger group. This is because ``dmp_`` functions
use ``dup_`` function to terminate recurrence, as ``dmp_`` implement dense recursive representation.

Suppose we want to implement a function for computing Taylor shifts. Given a univariate polynomial
$f$ in $\K[x]$, where $\K$ is an arbitrary domain, and a value $a \in \K$, we call a Taylor shift an
evaluation of $f(x + a)$. For details of the algorithm refer to [Nijenhuis1978combinatorial]_. To focus
our attention, we will show a sample implementation Taylor shift algorithm only for dense polynomial
representation. The implementation may be as follows::

    @cythonized('n,i,j')
    def dup_taylor(f, a, K):
        """Evaluate efficiently Taylor shift ``f(x + a)`` in ``K[x]``. """
        f, n = list(f), dup_degree(f)

        for i in xrange(n, 0, -1):
            for j in xrange(0, i):
                f[j+1] += a*f[j]

        return f

We defined a function called ``dup_taylor`` which takes three arguments: ``f``, ``a`` and ``K``. We
followed here the standard convention of L0 level, where ``dup_`` prefix tells us that the function
uses dense polynomial representation and allows only univariate polynomials. In the arguments list,
the first argument is an input polynomial, the second is evaluation point $a$ and the last one is
the coefficient domain. If a function requires two polynomials as input, e.g. multiplication function,
then the first two arguments are polynomials and other arguments come next. However, the domain is
always the last one (not counting optional or keyword--only arguments, which are rarely used on
this level).

This was for dense univariate polynomials. The convention for other groups of functions varies a
little bit. In the case of dense multivariate polynomials we add an additional argument ``u``, which
always goes before the ground domain, and stands for the number of variables of the input polynomial
minus one. Thus we get zero for univariate polynomials, which is convenient, because in the univariate
case, we can efficiently check that the polynomial is really univariate and fallback to the equivalent
univariate function to terminate recurrence. In the case of sparse distributed polynomials we add
another argument ``O``, besides ``u``, which goes between ``u`` and ``K``, and stands for a function
that defines an ordering relation between monomials (more about monomial orderings can be found in
section :ref:`thesis-orderings`).

A very special case is the group of ``gf_`` functions, which are used for computations with polynomials
over finite fields. The convention in this case is that the domain ``K`` is some domain representing
the ring of integers, not finite fields. We add an additional argument ``p``, which goes before ``K``
and stands for the size of the finite field (modulus). This, somehow awkward convention, has purely
historical background, because when L0 level was invented there were no ground domains in |sympy|, so
the argument ``p`` was the way to pass knowledge about the finite field, in which computations are
done, to ``gf_`` function. When ground domains were added to |sympy|, then it was too costly at that
time to remove argument ``p`` and use finite field domains instead of integer ring domains. It was
also uncertain if such move would not add too much overhead and slowdown ``gf_`` functions. A study
is needed to show if there is any advantage at all of having separate group of functions for the
special case of finite fields. Possibly in near future ``gf_`` functions will be merged with ``dup_``
functions, and ``gf_`` will be transformed to a suffix, because still finite fields are special
because specialized algorithms are needed for performing computations over this domain.

The first level: L1
-------------------

This is the second level in polynomials manipulation module and the last level used for internal
purpose. It is implemented in object--oriented style and wraps up functionality of the lowest
level into four classes: ``GFP``, ``DUP``, ``DMP`` and ``SDP``. Each class has methods which
reflect functions of L0 level, but with prefixes stripped. Also method call convention changes,
because ground domain and other properties are included in instances of L1 classes and provided
only on class initialization. This makes usage of functionality exposed by this level more
efficient, because the code is not that verbose as on the lowest level. L1 also implements
several other classes which provide more general computational tools, e.g. ``DMF`` for dense
multivariate fractions and ``ANP`` for a representation of algebraic numbers.

Classes of L1 level add tiny overhead over L0 functions, because L1 allows for unification
polynomials if they have different ground domains and there is additional constant time
needed to construct instances of L1 classes. In general in |sympy| we allow only immutable
classes, so instantiation overhead is added with every computation.

The main task for L1 level, besides wrapping up functionality of the lowest level, is to
provide types (classes) which can be used in composite ground domains, i.e. polynomial,
rational function and algebraic domains. We could use for this purpose tools of levels L2
and L3, but overhead associated with them would be too significant and thus computations
with composite ground domains would be very inefficient. This way levels L0 and L1 define
a self contained computational model for polynomials, which is later wrapped in much more
user friendly levels L2 and L3, which we will describe next.

The second level: L2
--------------------

This is the first level in polynomials manipulation module that is oriented towards the end
user. We implement only one class in L2, :class:`Poly`, which wraps up by composition ``GFP``,
``DUP``, ``DMP`` and ``SDP`` classes of L1. We call L2 classes, in this setup, polynomial
representations. :class:`Poly` implements the union of all functions that are available in L2
classes. If a certain operation is not supported by the underlying polynomial representation
then :exc:`OperationNotSupported` exception is raised.


The third level: L3
-------------------

The :class:`Poly` and all functions of L3 are called the public API of polynomials manipulation
module.

Motivation for multiple--level design
-------------------------------------

Suppose we are given a univariate polynomial with integer coefficients:

.. math::

    f = 3 x^17 + 3 x^5 - 20 x^2 + x + 17

We ask what is the value of $f$ at some specific point, say $15$. We can achieve this by
substituting $15$ for $x$ using :func:`subs` method of ``Basic``. This might not seem to
be the optimal solution for the problem, because :func:`subs` does not take advantage of
the structure of the input expression, just applies blindly pattern matching and SymPy's
built--in evaluation rules. But this is the first thing we can come out with. Lets try it::

    >>> f = 3*x**17 + 3*x**5 - 20*x**2 + x + 17

    >>> f.subs(x, 15)
    295578376007082351782

As the solution we obtained a very large number which is greater than $2^64$, i.e. can't fit
into CPU registers of modern machines. This is not an issue, because SymPy reuses Python's
arbitrary length integers, which are only bounded by the size of available memory. The size
of the computed value might, however, raise a question concerning the speed of evaluation. As
we said, :func:`subs` is a very naive function. Lets see how fast it can be::

    >>> %timeit f.subs(x, 15);
    1000 loops, best of 3: 992 us per loop

We used ``%timeit`` magic function from IPython. It adaptively chooses the right number of
function executions, so that we don't have to wait ages but also we get comprehensive timings.

It takes :func:`subs` about one millisecond to compute $f(15)$. This seems not that bad at all,
especially in an interactive session. Lets check if we get the same behaviour for much larger
evaluation points::

    >>> %timeit f.subs(x, 15**20);
    1000 loops, best of 3: 1.03 ms per loop

We chose a relatively large number $15^20$ for this test and obtained increase in evaluation
time by a very small fraction. This is still fine in an interactive session, but would it be
acceptable if :func:`subs` was used as a component of another algorithm? Lets consider a more
demanding example. We now use :func:`random_poly` function to generate polynomials of large
degree to see how :func:`subs` scales when the size of the problem increases::

    >>> g = random_poly(x, 1000, -10, 10)

    >>> %time g.subs(x, 15);
    CPU times: user 7.03 s, sys: 0.00 s, total: 7.03 s
    Wall time: 7.20 s

This time the results are not encouraging at all. We had to switch to IPython's ``%time`` magic
function for timing this evaluation only once, because it would take too long to use ``%timeit``
here. As all timings are done without caching mechanism and in a stable environment, were safe
to get correct timings. The resulting $7$ seconds, for a polynomial of the degree $1000$ with
integer coefficients bounded by $-10$ and $10$, are not acceptable even in an interactive
session.  It gets even worse if we do the computation using the larger evaluation point::

    >>> %time g.subs(x, 15**20);
    CPU times: user 9.88 s, sys: 0.04 s, total: 9.91 s
    Wall time: 10.29 s

Can we do better than this? To improve this timing we need to take advantage of the structure
of the input expressions, i.e. recognize that both $f$ and $g$ are univariate polynomial with
a very simple kind of coefficients (integers). All this is very important information, because
we can pick up an optimized algorithm for this particular domain of computation. A well known
algorithm for evaluating univariate polynomial is Horner's scheme, which is implemented in
:func:`eval` method of :class:`Poly` class. Lets rewrite $f$ and $g$ as polynomials and redo
the timings::

    >>> F = Poly(f)
    >>> G = Poly(g)

    >>> %timeit F.eval(15);
    10000 loops, best of 3: 34.3 us per loop

    >>> %timeit F.eval(15**20);
    10000 loops, best of 3: 43.1 us per loop

    >>> %timeit G.eval(15);
    1000 loops, best of 3: 1.02 ms per loop

    >>> %timeit G.eval(15**20);
    100 loops, best of 3: 16.4 ms per loop

We used :class:`Poly` to obtain polynomial form of $f$ and $g$, arriving with polynomials $F$
and $G$ respectively. We can clearly see, especially in the case of large degree polynomial,
that :func:`eval` introduced a significant improvement in computations time. This is not an
accident, because :func:`eval` uses a dedicated algorithm for the task and, what is currently
not visible, takes advantage of GMPY library, a very efficient library for doing integer
arithmetics. This may be considered a cheat, so lets force :class:`Poly` to compute with
SymPy's built--in integer type::

    >>> from sympy.polys.algebratools import ZZ_sympy

    >>> FF = Poly(f, domain=ZZ_sympy())
    >>> GG = Poly(g, domain=ZZ_sympy())

    >>> %timeit FF.eval(15);
    1000 loops, best of 3: 226 us per loop

    >>> %timeit FF.eval(15**20);
    1000 loops, best of 3: 283 us per loop

    >>> %timeit GG.eval(15);
    100 loops, best of 3: 15.7 ms per loop

    >>> %timeit GG.eval(15**20);
    10 loops, best of 3: 123 ms per loop

We obtained a visible slowdown, but we are still much faster that when using :func:`subs`.
A careful reader would argue that those timings are cheating once again, because we did not
take in to account the construction times of :class:`Poly` instances. Lets check if this is
significant::

    >>> %timeit Poly(f);
    100 loops, best of 3: 6.54 ms per loop

    >>> %timeit Poly(g);
    1 loops, best of 3: 1.79 s per loop

Indeed, construction of polynomials in this setup seems a very time consuming procedure. In
the case of the expression $f$ we do even worse that when using :func:`subs` alone. In the
later case we are still better, but the difference is not that impressive anymore. Although
this timing might look fine to the reader, it is a complete non--sense in this comparison,
because :class:`Poly` class constructor expands the input expression by default and this
step takes majory of time::

    >>> %timeit G = Poly(f, expand=False)
    1000 loops, best of 3: 209 us per loop

    >>> %timeit G = Poly(g, expand=False)
    10 loops, best of 3: 20.2 ms per loop

We know that $f$ and $g$ are already in the expanded form, so we can safely set ``expand``
option to ``False`` and completely skip the expansion step. This gives us a significant
speedup, when compared to the previous timing. More about constructing polynomials from
expressions will be said later in this chapter.

We can obtain a lower bound on univariate polynomial evaluation time in pure Python (up to
coefficient arithmetics), by transforming a polynomial into a string with valid Python code,
compiling it in ``eval`` mode and, finally, evaluating it using built--in :func:`eval`. To
do this, first we define a function :func:`poly_to_str`::

    def poly_to_str(poly, point):
        return '+'.join([ "%r*%r**%r" % (coeff, point, degree)
            for ((degree,), coeff) in poly.rep.to_dict().iteritems() ])

which will allow us to perform the conversion. Next we need to import ``mpz`` type from
GMPY library, because this is the default coefficient representation in SymPy, when GMPY
is available (which we assume is true)::

    >>> from gmpy import mpz

Normally this step would not be necessary, because ``mpz`` type is encoded in ``ZZ`` ground
domain, however, we will be working with raw string representations of types, so we need this
for the compilation phase. Finally we can compute the lower bound::

    >>> F_string = poly_to_str(F, ZZ(15))

    >>> %timeit poly_to_str(F, ZZ(15));

    >>> F_compiled = compile(F_string, '<input>', 'eval')

    >>>

Excluding transformation and compilation steps, the lower bounds are

::

    def evaluate(f, point):


    In [3]: f3 = product(x-k, (k, 1, 10))

    In [4]: f2 = Poly(f3)

    In [5]: f1 = f2.rep

    In [6]: f0 = f1.rep

    In [7]: timed(lambda: factor_list(f3))
    Out[7]: (10, 0.052675819397, 52.675819397, ms)

    In [8]: from sympy.polys.factortools import dup_factor_list

    In [9]: from sympy.polys.polyclasses import DMP

    In [10]: timed(lambda: factor_list(f3))
    Out[10]: (10, 0.0526403188705, 52.6403188705, ms)

    In [11]: timed(lambda: f2.factor_list())
    Out[11]: (10, 0.0243428945541, 24.3428945541, ms)

    In [12]: timed(lambda: f1.factor_list())
    Out[12]: (10, 0.024045085907, 24.045085907, ms)

    In [13]: timed(lambda: dup_factor_list(f0, ZZ))
    Out[13]: (10, 0.0238025903702, 23.8025903702, ms)

    In [14]: %timeit factor_list(f3)
    10 loops, best of 3: 53.2 ms per loop

    In [15]: %timeit f2.factor_list()
    10 loops, best of 3: 24.8 ms per loop

    In [16]: %timeit f1.factor_list()
    10 loops, best of 3: 24.2 ms per loop

    In [17]: %timeit dup_factor_list(f0, ZZ)
    10 loops, best of 3: 24.2 ms per loop

    In [18]: %timeit dup_factor_list(f0, ZZ)
    10 loops, best of 3: 24.1 ms per loop

    In [19]: %timeit dup_factor_list(f0, ZZ)
    10 loops, best of 3: 24.3 ms per loop



Polynomial representations
==========================

SymPy implements two major polynomial representations: dense and sparse. A polynomial
representation is a specialized data structure that is used for storing the structure
of a polynomial and its coefficients. Metadata, e.g. ground domain information, is not
considered as a part of a polynomial representation and is stored separately.

In the case of univariate polynomials SymPy implements both representations as true dense
and sparse representations, i.e. as a list of all coefficients (including zeros) and a
dictionary of exponent, non--zero coefficient pairs, respectively. The multivariate setup
is much more complicated, because implementing a true dense representation is not feasible.
If we have a polynomial of the total degree $n$ in $k$ variables, then the number of monomials
of such a polynomials is as large as $\frac{(n + k)!}{n! k!}$. For example, if $n = 50$

There is ultimate polynomial representation that would fit to all problems.

Dense polynomial representation
-------------------------------

This is currently the main polynomial representation

The univariate case
~~~~~~~~~~~~~~~~~~~

The multivariate case
~~~~~~~~~~~~~~~~~~~~~

1. GFP repr: [c_n, ..., c_0]

     spec: gf_some_function(f, g, p, K)

     where p is prime >= 2, type int
           K is any ZZ algebra

2. DUP repr: [c_n, ..., c_0]
     spec: dup_some_function(f, g, K)

     where K is any algebra

3. DMP repr: [[...], [...], ..., [...]]
     spec: dup_some_function(f, g, u, K)

     where u is number of nested levels - 1
           K is any algebra

     DMP for u = 0 is DUP

Sparse polynomial representation
--------------------------------

Currently this is the auxiliary polynomial representation that is mainly used for computing
|groebner| bases. This is because it allows for using different orderings of monomials, which
is an important part of Buchberger algorithm.

The univariate case
~~~~~~~~~~~~~~~~~~~

In the univariate case the sparse polynomial

The multivariate case
~~~~~~~~~~~~~~~~~~~~~


4. SDP repr: [(M_n, c_n), ..., (M_0, c_0)]
     spec: dup_some_function(f, g, u, O, K)

     where u is number of variables - 1
           O is monomial order function
           K is any algebra

Comparing speed of both representations
---------------------------------------



This clearly indicates that sparse representation should be used as the main polynomial
representation in near future, because it works better in the average case, especially
when the

Categories, domains and types
=============================

To understand and use the properties of the coefficient domain (computation domain, ground domain)
we need to somehow extract information about the common nature of all coefficients and store this
information in some data structures. This is crucial for optimizing speed of computations, because
the more we know about the domain, the better algorithms we can pick up for doing the computations.

Motivation
----------

Suppose we perform computations with polynomials that have coefficients in the ring of integers.
    So, lets suppose we want to compute in integers ring. Then we have
    a category ZZ, which is supposed to have binary operations +, -
    , functions like gcd(), lcm() etc. and some properties. On the
    other side we have several data types for integers: Python (int),
    SymPy (Integer) or gmpy (mpz), or maybe even something else. Each
    of these has different algorithms implemented and have different
    interfaces, e.g. int does not implement gcd(), which is however
    implemented by Integer and mpz. On the other hand int and mpz
    are fast, but Integer is very slow.


Basic definitions
-----------------

The type system

category
    Category is the most general bit in the type system of SymPy's polynomials manipulation
    module. It defines the mathematical properties and the interface that concrete domains
    will implement. Categories are abstract classes which are inherited by domains. Examples
    for categories are.

    Ring
    Field
    IntegerRing,
    RationalField,
    PolynomialRing
    FractionField


domain
    Domain is a

    Domain encapsulates functionality provided by a type. This way we can use different
    types and have a single, unified interface to all of them.

type
    Type is a raw implementation of the of a particular domain. Types are system specific
    and

    Types are usually provided by third--parties and SymPy's developers

    For example ``int`` is a built--in Python's type, which implements the standard interface
    for numeric types, i.e. arithmetics operators: ``__add__``, ``__mul__``, ..., and some
    functions e.g. ``__abs__``.

    This is only a partial interface, as, for example, :func:`gcd` method is missing. Python
    also does not provide :func:`gcd` function in the standard library.

The API for constructing domains
--------------------------------

All domains in SymPy are classes, so to construct a domain the user needs

Automatic selection of an optimal domain
----------------------------------------

It would be tedious to always specify the ground domain manually via ``domain`` option. However,
when constructing a polynomial, e.g. from an expression, SymPy can figure out the best domain
that contains all coefficients of the input polynomial.


Motivation
----------


Python is a dynamically typed programming language and its users expect for it a

    Polynomial manipulation algorithms understand algebraic properties
    of elements of a ground domain (polynomial coefficients). For this
    purpose additional module was implemented to define all important
    coefficient domains (the only missing is for algebraic numbers).

    Basically the world is divided into to parts: types and categories
    (here algebras or domains). Type is an object which caries data
    and is equipped with algorithms for processing this data in some
    way using some paradigm for this purpose. Different types have
    different algorithms and use different paradigms. However from
    mathematical point of view there are categories which have some
    properties and don't care about internal behavior of a data type.

    To have one source base of algorithms we specify a category for
    a mathematical concept for each data type we want to have, e.g.
    we have (in algebratools.py) ZZ_python, ZZ_sympy and ZZ_gmpy
    which implement Ring interface which is based on Algebra
    abstract class.

    You can use any of ZZ_* classes as coefficient domains in new
    polynomials module, by creating instances of those classes. Or
    you can just

              from sympy.polys.algebratools import ZZ

    to get optimal solution for your system (ZZ is an instance).

    Then if a function gets as parameter K algebra ZZ, then it knows
    that all coefficients given in a polynomial representation to this
    function have type ZZ.dtype (e.g. int) and know that int is supposed
    to provide some methods, e.g. __add__ and that ZZ wraps some other
    methods, e.g. ZZ.gcd is really igcd from sympy.core.numbers.

    The same is for other domains: QQ, ZZ[x,y], ZZ(x,y,z), QQ('x') ...

    There is also one category above all others: EX, which is a wrapper
    for SymPy expressions. If Poly can't figure out an optimal domain
    or such domain in not yet implemented (e.g. algebraic numbers),
    then it uses EX. EX is slow, but tries to do its best to solve
    zero equivalence problem in a symbolic way (by calling simplify).

    On L2 level you don't have to care about domains at all. Poly will
    figure out a domain or fallback to EX. However, when implementing
    algorithms that require certain algebraic properties to be met, be
    specific or you loose the battle. The most important thing is
    to see a difference between computations over a ring and a field,
    which can cause you a lot of trouble. So, don't hack and use
    the interface, e.g. don't gcd(), div(), div() but cancel() and
    it will take care of all weird cases.

    To specify a domain simply add `domain` keyword argument. Note
    you need also to specify generators when this kwarg is given
    (this will change in future) e.g.

                 Poly(x**2*y + z, x, y, domain='ZZ[z]')

    Domain can be specified as a string or explicit algebra. Allowed
    strings are 'GF(p)' where p is prime, 'ZZ' or 'Z', 'QQ' or 'Q',
    'ZZ[x,y,z]', 'QQ[x,y,z]', 'ZZ(x,y,z'), 'QQ(x,y,z)' and 'EX'. Or

               from sympy.polys.algebratools import ZZ

    and ZZ[x,y,z] or even ZZ['x','y','z'] will work. Each algebra
    implements __getitem__ for this, which fallbacks to poly_ring
    method. Note that __call__ is used for very different purpose,
    so don't get tricked, use ZZ.frac_field(x,y,z) or a convenient
    string representation.

    If you don't want to specify an exact domain but you know
    computation has to be done in a field then pass `field=True`
    to Poly or any polynomial function to force a Field to be
    chosen rather than a Ring. By default if Poly sees that
    coefficients fall into a Ring it will choose it, e.g.

               Poly(x**2 + 1) will have the domain ZZ

    but

               Poly(x**2 + 1, field=True) will have QQ

    Despite that if a function needs a field then it will silently
    convert to field and continue computations. To disable this
    set `auto=False`. Don't complain if you get DomainError or
    ExactQuotientFailed exceptions. This automatic behaviour is
    available only on L2 level. On other levels no auto-games are
    played by polynomial manipulation algorithms and if there is
    an inappropriate domain of computation specified, algorithm
    will just fail, raising an exception.

    If you want to compute in Galois fields then specify `modulus`
    keyword argument. Note that only univariate polynomials are
    supported and some methods might not be implemented (you will
    get OperationNotSupported exception). Alternatively specify
    `domain='GF(p)'` where `p` is a prime integer.

    Note that when parsing expressions Poly will treat everything
    which is not a number as a generator. This way

                     gcd(x**2 - 2, x - sqrt(2))

    is 1, not x - sqrt(2). Specify generators to override this behaviour.
    In future `extension` keyword might be included to notify algorithms
    about algebraic relations between coefficients.


   Use gmpy by default in polys and show types at init

    Previously the default ground types were Python's int and Fraction
    types (or SymPy's Rational on 2.4 / 2.5). The new default is gmpy,
    if gmpy is available. If not SymPy will fallback to slower types
    as previously.

    To cut down on confusion what ground types are being used in a
    particular session, the information about ground types that were
    setup is now displayed in the welcome message in isympy. The text
    is in a form: "types: something" (as it is done with cache).

    If SymPy was able to use the same types for both ZZ and QQ domains,
    then 'something' will be set to 'gmpy', 'python' or 'sympy'. If this
    is not the case, e.g. in 2.4 w/o gmpy, then SymPy uses mixed ground
    types and 'something' will be in a form: "ZZ_type/QQ_type". In the
    example given it would be "types: python/sympy", i.e. ZZ.dtype is
    int and QQ.dtype is Rational.

    Examples:

    1. Python 2.6 with gmpy

    $ python2.6 bin/isympy -q
    IPython console for SymPy 0.6.7-git (Python 2.6.2) (types: gmpy)

    2. Python 2.6 w/o gmpy

    $ SYMPY_GROUND_TYPES=python python2.6 bin/isympy -q
    IPython console for SymPy 0.6.7-git (Python 2.6.2) (types: python)

    3. Python 2.4 w/o gmpy

    $ python2.4 bin/isympy -q
    Python console for SymPy 0.6.7-git (Python 2.4.4) (types: python/sympy)

Transforming expressions into polynomials
=========================================

Before the user can take advantage of efficient algorithms and data structures for polynomials
manipulation, expressions that are involved in computations have to be transformed to a form
that is understood in polynomials manipulation module. This transformation is called expression
parsing. The reason why such step is necessary, when constructing polynomials, is that the
internal representation of an expression is different from a representation of a polynomial
representing this expression and does not take into account many polynomial related properties,
like generators or coefficient domain. With expression parser we can understand the structure
of an expression and construct a polynomial representation for it.

Expression parsing
------------------

_dict_from_basic_if_gens
_dict_from_basic_no_gens


Greedy vs. non--greedy parsers
------------------------------

By default, everything that is not an explicit number (an instance of ``Number`` class) is
treated as a potential generator of a polynomial.

Speed related issues
--------------------

Depending on the size of an input polynomial and the coefficient domain, expression parsing
make take considerable amount of time.

Polynomial unification
======================

Public APIs of the module
=========================

Private APIs of the module
==========================

Managing contexts of evaluation
===============================

Adjusting the internal configuration
====================================


Previously there were two methods used for configuring what
algorithms should be used and how they will perform:

1. Passing keyword arguments around.
2. Setting up global variables.

Now there is only one configuration approach, via polyconfig.

Consider the following example:

In [1]: from sympy.polys.polyconfig import query, setup

In [2]: query("USE_CYCLOTOMIC_FACTOR")
Out[2]: True

In [3]: %time u = factor(x**100 - 1)
CPU times: user 0.04 s, sys: 0.00 s, total: 0.04 s
Wall time: 0.05 s

In [5]: setup("USE_CYCLOTOMIC_FACTOR", False)

In [6]: %time u = factor(x**100 - 1)
CPU times: user 2.66 s, sys: 0.01 s, total: 2.66 s
Wall time: 2.75 s

To reset configuration to the default

In [8]: setup("USE_CYCLOTOMIC_FACTOR")

In [9]: %time u = factor(x**100 - 1)
CPU times: user 0.05 s, sys: 0.00 s, total: 0.05 s
Wall time: 0.05 s

This way several low-level algorithms can be configured and, for
example, benchmarking or algorithm parameters optimization was
made a lot easier.

.. _thesis-cython:

Using Cython internally
=======================

Cython (www.cython.org) is a general purpose programming language that is based on Python
(shares very similar syntax), but has extra language extensions to allow static typing and
allows for direct translation into optimized C code. Cython makes it easy to write Python
wrappers to foreign libraries for exposing exposing their functionality to interpreted code.
It also allows to optimize pure Python codes, which we take advantage of.

There are two approaches to enhance software speed that is written in pure Python. The first
is to rewrite carefully selected parts of Python code in Cython and compile them. Depending
on the quality of Cython code, speed gain might vary, but, in any case, will be substantial
over the pure Python version. This approach has the benefit that developers have complete
control over the optimizations that are used. However, one has to provide two source bases
for optimized parts of the system, which makes maintenance and future extensions complicated.
This makes direct Cython usage a measure of last resort when optimizing Python codes.

The other approach is to use, so called, *pure mode* Cython. This a very recent development
in Cython, which allows the developers to keep a single source base of pure Python code, while
still benefiting from translation to machine code level, gaining speed improvement. Single source
base is achieved by simply decorating functions or methods with a special decorator, which marks
a function or method as compilable. The decorator also allows to specify which variables will be
considered as native and which will remain pure Python variables. It is also possible to declare
the type of each native variable. Then the decorated code can be run as normally in a standard
Python interpreter, of course without any speed gain, but, what is more important, without any
speed degeneracy (Cython decorators are empty decorators in interpreted mode). To take advantage
of Cython, the user has to compile selected modules with Cython compiler, which results in a
dynamically linked library (e.g. ``*.so`` on Unix platforms and ``*.dll`` on Windows) for each
compiled module. During the next execution of the system, Python interpreters will select compiled
modules in favour to the pure Python ones.

It should be clearly understood that if a variable is marked as native, then it conforms to the
rules of the platform for which the code was compiled. If we declared, for example, a variable
to be of integer type (C's ``int`` type), then there will be restriction of on the size of values
accepted by such variable. There is no overflow checking or automatic conversion to arbitrary
length integers, so one has to be very careful about which variables are marked as native to
avoid faulty code on certain platforms.

Pure mode Cython in SymPy
-------------------------

To reduce the overhead of using pure mode Cython in SymPy to minimum, ``@cythonized`` decorator
was introduced, which wraps original Cython's decorators and adjusts them to SymPy's needs. This
is useful because we don not take advantage of many advanced Cython's features. The only feature
we need is to mark variables as native, because all native variables in SymPy, at least at this
point, are integers, so there is not need to make things unnecessarily complicated. The decorator
also allows to run SymPy in interpreted mode without Cython installation on the system. To achieve
this, which is one of fundamental SymPy's goals, we simply try import Cython and when this is not
possible, we simply define an empty decorator.

Suppose we implement a function for rising a value to the $n$--th power, :func:`power` in this case.
For this task we employ classical repeated squaring algorithm. A sample implementation goes as follows::

    @cythonized('value,result,n,m')
    def power(value, n):
        """Raise ``value`` to the ``n``--th power. """
        if not n:
            return 1
        elif n == 1:
            return value
        elif n < 0:
            raise ValueError("negative exponents are not supported")

        result = 1

        while True:
            n, m = n//2, n

            if m & 1:
                result *= value

                if not n:
                    break

            value **= 2

        return result

The function can be run in both interpreted and compiled modes. To tell Cython that :func:`power`
is ready for compilation, we use ``@cythonized`` decorator, in which we declare four variables as
native: ``value``, ``result``, ``n`` and ``m``. All four will have ``int`` type assigned during
translation to C code. Two of those variables are input to the function. Cython is enough clever
to automatically convert Python integers to native integers if necessary. The same can happen the
other way in ``return`` statement. It is important to note that in interpreted mode Python uses
arbitrary length integers, so we can compute arbitrary powers using :func:`power` function. This
situation changes in compiled mode because we are restricted by machine types --- we can store
at most 32--bit or 64--bit values in native variables, depending on the actual architecture for
which this piece of code was compiled. Such difference can have serious consequences, like wrong
results of computation, if pure mode Cython was used without understanding of the behavior of this
code on different platforms. This shows that developers have to be very careful about which variables
should and which should not be marked as native. The general advice is to use native variables for
loop indexes and auxiliary storage which we can guarantee to remain in right bounds. There are,
however, cases where native variables can be used for doing actual computations, because it
might be unrealistic to use larger values that 32--bit long. A good example is :func:`divisors`,
which computes all divisors of an integer.

In polynomials manipulation mode we marked all loop index variables and some auxiliary variables on
the lowest level as native. At this moment no coefficient arithmetics is done natively. It would be,
however, very convenient in future to take advantage of native coefficient arithmetics when computing
with polynomials over finite fields. In most practical cases in SymPy, coefficients which arise over
finite fields are half--words, so arithmetics (especially including multiplication) can be done in a
single machine word (32 bits). We could also consider allowing 64--bit words, if architecture supports
this, to widen the range of application of optimized routines.

To take advantage of Cython in SymPy, the user has to compile it. By default SymPy ships only with
bytecode modules and scripts for compiling them, if Cython is installed on the system. Assuming
that GNU make is installed, then compiling SymPy is as simple as typing ``make`` at a shell prompt
in the main directory of SymPy source distribution. If GNU make is not available, then the user
has to issue the following command::

    python build.py build_ext --inplace

from the same directory. This command tells Cython to compile all modules in SymPy, which have
functions or methods marked with ``@cythonized`` decorator. The compilation is done in--place,
meaning that there will two additional files for each Python source file: ``*.pyc`` file with
bytecode and a compiled dynamically linked library. If ``--inplace`` was omitted, then Cython
would store compiled modules in a separate directory, which would make running SymPy with
compiled modules complicated.

Benchmarking pure mode Cython
-----------------------------

It is very cheap to employ pure mode Cython in Python code. Does it, however, bring any improvement
over pure Python? First experiments with pure mode Cython, which we conducted in SymPy, showed that
the befit can be substantial or even impressive, giving over 20 times speedup for particular small
functions, in which we could use native variables for coefficient arithmetics. The main subject of
those experiments was :func:`divisors`` function. Those experiments were, however, artificial and
for real--life cases speedup is not that big, but still worthy consideration, especially we take
the tiny cost of pure mode Cython (one additional line per function or method).

Suppose we expand a non--trivial expression $((x + y + z)^15 + 1) \cdot ((x + y + z)^15 + 2)$ and
then we want to factor the result back. We are interested only in factorization time. We perform
the same computation in pure Python and pure mode Cython:

* pure Python
    ::

        >>> f = expand(((x+y+z)**15+1)*((x+y+z)**15+2))

        >>> %time a = factor(f)
        CPU times: user 109.45 s, sys: 0.01 s, total: 109.47 s
        Wall time: 110.83 s

        >>> %time a = factor(f)
        CPU times: user 109.31 s, sys: 0.03 s, total: 109.34 s
        Wall time: 110.68 s

* pure mode Cython
    ::

        >>> f = expand(((x+y+z)**15+1)*((x+y+z)**15+2))

        >>> %time a = factor(f)
        CPU times: user 72.09 s, sys: 1.02 s, total: 73.11 s
        Wall time: 74.18 s

        >>> %time a = factor(f)
        CPU times: user 72.81 s, sys: 0.04 s, total: 72.85 s
        Wall time: 73.74 s

We can see that for this very particular benchmark we obtained 1.5 times speedup. This is
not 20 times, but still can be considered important, especially when such long computation
times are involved. More throughout timings can be found in figures :ref:`fig-cython-power`
and :ref:`fig-cython-factor`, where we exponentiated and factored polynomials for various
exponents and degrees, respectively.

.. _fig-cython-power:
.. figure:: ../img/plot/cython-power.*
    :align: center

    Benchmark: exponentiation of $(27 x + y^2 - 15 z)^n$.

.. _fig-cython-factor:
.. figure:: ../img/plot/cython-factor.*
    :align: center

    Benchmark: factorization of $x^n - 1$ over integers.

In future we expect even better improvements when native variables will be used for coefficient
arithmetics. Every algorithm which uses modular approach, which include algorithms for factoring
polynomials, computing GCD or resultants, will benefit from this, because coefficients arising
on the intermediate steps in those algorithms are usually half--words (computations are done in
small finite fields). How to achieve this, without compromising functionality and correctness,
is a subject for future discussion.

