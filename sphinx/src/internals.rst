.. include:: ../globals.def

.. _thesis-internals:

====================================
Notes on the Internal Implementation
====================================

Knowing the goals of the project, lets now focus on the internal implementation of polynomials
manipulation module and methods that were used to reach the goals. In this chapter we will
describe step--by--step all details concerning the design and implementation of them module,
from the technical point of view. In the next chapter we will jump in the implemented algorithms.

Physical structure of the module
================================

Polynomials manipulation module consists of a

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
    Tools for managing context of evaluation.

``sympy/polys/polyerrors.py``
    Definitions of polynomial specific exceptions.

``sympy/polys/polyoptions.py``
    Managers of options that can used with the public API.

``sympy/polys/polyroots.py``
    Algorithms for root finding via radicals.

``sympy/polys/polytools.py``
    The public API of polynomials manipulation module.

``sympy/polys/polyutils.py``
    Internal utilities for expression parsing, handling generators etc.

``sympy/polys/rootisolation.py``
    Low--level algorithms for symbolic real and complex root isolation.

``sympy/polys/rootoftools.py``
    Tools for formal handling of polynomial roots: ``RootOf`` and ``RootSum``.

``sympy/polys/specialpolys.py``
    A collection of functions for generating special sorts of polynomials.

In future, ``algebratools.py`` will be split into smaller source files and put into a separate
directory ``ground`` in ``sympy/polys``.

Logical structure of the module
===============================

One of the main concerns when designing a symbolic manipulation library, especially one which is
written in an interpreted general purpose programming language, is speed. Even the best equipped
library, with most recent, cutting edge algorithms and data structures, user friendly API and
easily configurable internals, has little value if the user needs to wait ages for any, even a
trivial, result. This was recently the main problem with |sympy| in general and its fundamental
weakness . It should be clearly understood that code written in an interpreted language will be
always slower than compiled code, unless we had a very clever JIT (Just--In--Time) compiler which
could optimize and compile the code on--the--fly. However, this shouldn't be discouraging and we
are supposed to put our best efforts to make |sympy| as fast as possible, especially when
implementing the infrastructure which is used everywhere else in the library.

There is a trivial observation about interpreted programming languages: there is a very high cost
associated with every function call and with every use of *magic* functionality of the language of
choice. This statement is true in the general case of interpreted languages and the first part is
especially true in the case of Python programming language. There is another observation concerning,
this time, algorithms of symbolic mathematics: often they require very large number of function calls.
The number varies between different algorithms, but for the most complex ones, the number can be as
high as millions (or more) function calls per algorithm execution.

One obvious (in theory) solution to this problem is to use *better* algorithms. Unfortunately, it
is not clear what we mean by better in this context. If we take only pure algorithmic complexity
of methods we implement in |sympy|, then one could argue that we should always implement polynomial
time algorithms, of course if they exist in particular areas. This would be a perfect solution,
however, there an interesting phenomenon occurs. Often polynomial time algorithms are slower than
their counter parts which exhibit exponential time. This is true, for example, in the case of polynomial
factorization algorithms where the LLL algorithm [Lenstra1982factor]_, the only known polynomial time
approach to polynomial factorization, is almost always slower than *efficient* exponential time algorithms.
Besides this phenomenon, whatever approach we take for choosing a good algorithm for implementation in
|sympy| for improving speed, there is a high cost associated with such event, because first one has to
assure correctness of the new development and only then think about improving speed. Of course, this is
what we do in |sympy| and a detailed discussion about algorithms will follow in the next chapter.

There is, however, another method for significantly improving computations speed. In parallel with
implementation of *better* algorithms, one can eliminate as much overhead as possible. The overhead
is associated with the cost of interpretation of program code. As we stated before, the cost of
function calls in Python is high, but the more *advanced* constructs of the language we use the
higher the cost is. However, the less *magic* we use the harder is to use the code, so our task
is to find the cross--over point, where we have both speed and usability in balance. This is
because speed without usability is as much pointless as usability without speed.

The answer to those observations is a design of polynomials manipulation module in a form of a
multiple--level environment, where on the lowest level are fundamental functions which are run
most often and form a computational basis for other levels which tend to be much more oriented
towards the user adding the cost associated with more user friendly API. Multiple--levels is
nothing new to symbolic mathematics and this is how things were done from the very beginning.
However, usually those levels were associated with usage of different programming languages,
where the core, which is usually not accessible directly by the user, is implemented in a
compiled language and the library (API) is written in a much more user friendly programming
language. |sympy| is written entirely in a single, interpreted programming language so we
introduce multiple levels in this one language, by selecting appropriate feature of the
language on each level.

In polynomials manipulation module, three levels were introduced: L0, L1 and L2. Each level
has its own syntax and API, and is used for different tasks in |sympy|. Redundancy between
levels is reduced to minimum, so that not a single algorithm is duplicated on any level. Also
tests are designed the way that they only test correctness of incrementally added functionality.

The zeroth level: L0
--------------------

This is the most inner level of polynomials manipulation functionality, which is used only for
internal purpose in the module. All code on this level is written in purely structural style and
no magic Python's functionality is used. We tried to choose only a minimal subset of functionality
of the module for implementation on this level. L0 is spread over several files in ``sympy/polys``
and implements two polynomial representations and most important algorithms:

* polynomial arithmetics
* gcd, lcm, square--free decomposition
* factorization into irreducibles
* real and complex root isolation
* |groebner| bases

Functions on this level are split into several groups, depending on which polynomial representation
they belong to and what kind of ground domain can be used with them. Currently there are four major
groups, which can be distinguished by their special prefixes:

``gf_`` --- univariate polynomials over Galois fields (finite fields)

``dup_`` --- dense univariate polynomials over arbitrary domains

``dmp_`` --- dense multivariate polynomials over arbitrary domains

``sdup_`` --- sparse distributed univariate polynomials over arbitrary domains

``sdmp_`` --- sparse distributed multivariate polynomials over arbitrary domains

There are additional minor suffixes which can be added to the major prefixes. They are used to tell
the difference between the same function, e.g. for computing the greatest common divisor, for various
ground domains. The typically used suffixes are ``zz_``, ``qq_``, ``rr_`` and ``ff_``, which stand
for the ring of integers, the rational field, any ring and any field, respectively. Note that those
suffixes are not combined with the ``gf_`` prefix. Usually function if a function comes with a suffix,
then it will be defined for both, either ``zz_`` and ``qq_``, or ``rr_`` and ``ff_``. There will be
also a function without any suffix, which will dispatch flow to an appropriate specialized function,
depending on the analysis of the ground domain. This separation is necessary, because it often happens
that functions for computing a particular quantity over different ground domains, have very different
semantics and internal structure. A good examples are functions for computing GCDs and factorizations
of polynomials. One should also note that even if there is a separation between different ground domains,
it is still possible (and it often happens) that a function for a more general domain will transform the
problem and run an algorithm for a smaller domain, to take advantage of more efficient algorithms.


Each type of polynomial: GFP, DUP, DMP, SDP, has a raw
representation and function call specification associated:

The first level: L1
-------------------

Is implemented using OO paradigm and wraps up functionality
provided by L0. For each type of polynomial there is a class
implemented: GFP, DUP, DMP, SDP. There are additional classes
for multivariate rational functions DMF and algebraic number
polynomials ANP (a representation of algebraic numbers).

Each class is constructed using an explicit representation and
algebra specification. Method calls will unify arguments by
coercing their ground domains (e.g. ZZ + QQ -> QQ), so there
is no need to specify any extra arguments.

Note that unification rules on this level are very simple so
e.g. operations on a univariate polynomial as one argument and
a multivariate polynomial as the other aren't allowed, unless
you make any coercions explicitly.

For efficiency, every class in L1 doesn't derive from Basic, which
allows to use those classes as representations of composite ground
domains e.g. ZZ[x,y,z], QQ(x,y).

The second level: L2
--------------------

User-level interface to polynomial manipulation algorithms. If
you are a user, then you choose this level, which provides you
convenient Poly class which wraps L1 classes as internal poly
representations but provides user-friendly interface. There
is also a set of public functions exported: gcd, lcm, factor
and many others.

Poly class allows you to convert a SymPy expression into a
polynomial. There is no need to specify symbols, Poly class
will parse the expression and figure out what are symbols
and what are members of the coefficient domain. Note also
that you can create polynomials using not only symbols but
any expressions, this way Poly.symbols was renamed to
Poly.gens, to emphasize this fact, so

             Poly(sin(x)**2 + 1, sin(x))

are valid arguments to Poly.__init__ and computing e.g.

           gcd(sin(x)**2 - 1, sin(x) - 1)

is also allowed.

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



Expression parsing
------------------

_dict_from_basic_if_gens
_dict_from_basic_no_gens

By default, everything that is not an explicit number (an instance of ``Number`` class) is
treated as a potential generator of a polynomial.

Greedy vs. non--greedy parsers
------------------------------

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

In [8]: setup("USE_CYCLOTOMIC_FACTOR")

In [9]: %time u = factor(x**100 - 1)
CPU times: user 0.05 s, sys: 0.00 s, total: 0.05 s
Wall time: 0.05 s

This way several low-level algorithms can be configured and, for
example, benchmarking or algorithm parameters optimization was
made a lot easier.


Using Cython internally
=======================

Cython [] is a general purpose programming language that is based on Python, but has extra
language extensions to allow static typing and allows for direct translation into optimized
C/C++ code. It makes easy to write Python wrappers for foreign libraries, but also it allows
to optimize pure Python code.

There are two approaches. The first is to rewrite selected parts in Cython and compile them.
Depending on the quality of Cython code, speed gain might vary, but, in any case, will be
substantial. This approach has the benefit that we can control the optimization and make it
better where ever possible. However, one has to provide to source bases for optimized parts
of the system, which makes maintenance and future extensions hard.

The other approach is to use, so called, pure mode Cython. This allows the developers to keep
a single source base, while still benefiting from translation to the machine code level, gaining
speed improvement. Pure mode can be very easily utilized in SymPy, because there is a simplified
interface provided

Employing Cython
----------------

Suppose we implement function for rising a value to the $n$--th power. We do this for the
general setup in pure Python to meet SymPy's goals. A sample implementation follows::

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

The function :func:`power` is

This means that `some_function` will be compiled by
Cython if available, treating variables n and k as
integers (cython.int). This is convenient because
currently we don't use any other types.

If Cython is not available then @cythonized is an
empty decorator (there is no performance penalty).

To take advantage of pure mode Cython, you have to
compile modules which support cythonization. To do
this, issue:

python build.py build_ext --inplace

in SymPy's root directory (or use make). Then run
isympy or import sympy as usually (compiled modules
will have priority over pure Python).

Cythonized zero-level algorithms in new polynomials module

Pure Python:

In [1]: f = expand(((x+y+z)**15+1)*((x+y+z)**15+2))

In [2]: %time a = factor(f)
CPU times: user 109.45 s, sys: 0.01 s, total: 109.47 s
Wall time: 110.83 s

In [4]: %time a = factor(f)
CPU times: user 109.31 s, sys: 0.03 s, total: 109.34 s
Wall time: 110.68 s

Pure mode Cython:

In [1]: f = expand(((x+y+z)**15+1)*((x+y+z)**15+2))

In [2]: %time a = factor(f)
CPU times: user 72.09 s, sys: 1.02 s, total: 73.11 s
Wall time: 74.18 s

In [4]: %time a = factor(f)
CPU times: user 72.81 s, sys: 0.04 s, total: 72.85 s
Wall time: 73.74 s

On average Cython version is two times faster than pure
Python. This is an improvement and hopefully it should
get even better in future.

To make cooperation with Cython more comfortable a new
decorator was added to sympy/utilities/cythonutils.py.

Example:


Using the module without SymPy
==============================



