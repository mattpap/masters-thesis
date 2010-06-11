.. include:: ../globals.def

.. _thesis-algorithms:

=================================================
Algorithms of the Polynomials Manipulation Module
=================================================

SymPy implements wide variety of algorithms for polynomials manipulation, which ranges from
polynomial arithmetics to advanced methods for factoring polynomials over algebraic number
fields or computing |groebner| bases. In this chapter we will give a short description to all
polynomial manipulation algorithms in SymPy. The descriptions will include a short note on the
purpose and applications of a particular algorithm, as well as discussion on its computational
complexity and possibility of parallelization. We will also give reference to most influential
papers, which were used for implementing polynomial related algorithms in SymPy.

Polynomials arithmetics
=======================

SymPy

The Greatest Common Divisor
===========================

GCD (Greatest Common Divisor) is a fundamental component of most

Functional decomposition
========================

Square--free decomposition
==========================

Factorization into irreducibles
===============================

Univariate polynomials
----------------------

* Integers and rationals
* Algebraic number fields
* Composite domains
* Other domains

Multivariate polynomials
------------------------

* Integers and rationals

    Improved Wang's algorithm to run in more deterministic time

    As the multivariate factorization algorithm (Wang's) was tested
    for correctness for multitude of inputs using different system
    configuration schemes (e.g. using gmpy as ground coefficients),
    now we can lower bounds for evaluation points of variables,
    when transforming multivariate problem to a univariate one.

    Now the algorithm will try to find three evaluation sets, such
    that all sets generate the same number of univariate factors
    after substitution. If a new set generates smaller number of
    factors, then all other are discarded and algorithm tries to
    find to other configurations with the same number of factors.

    If any of evaluation sets gives factor list of length one, then
    the input multivariate polynomial is irreducible and no further
    factorization is computed.

    The first evaluation set tried is always [0,0,...,0], to test
    if rare but very promising situation happens. Other evaluation
    sets are generated at random, modulo some integer. At first the
    algorithm generates sets modulo 1, i.e. in range [-1, 1], then
    modulo 2, i.e. in range [-2,2] and so on. For each modulus only
    5 evaluation sets are checked. If algorithm wasn't able to find
    three configuration that minimize number of univariate factors
    then it proceeds to the next modulus and continues searching.

    When three sets were found, then the algorithm chooses the one
    which generates, after substitution, the univariate polynomial
    of smallest max-norm. This is important because EEZ lifting
    algorithm is very sensitive to coefficient sizes. Univariate
    factorizations are only a small part of the total procedure
    execution time, so it might be convenient to try a few more
    factorizations to minimize further coefficients.

* Algebraic number fields
* Composite domains
* Other domains

|groebner| bases
================


Root isolation
==============

Polynomials are solvable by radicals only up to degree 4 (inclusive). This is an unfortunate
but well known consequence of Abel--Ruffini theorem. SymPy implements heuristic algorithms
for solving polynomials in terms of radicals in :func:`roots` function. In some cases it is
possible to find roots of higher degree polynomials, by taking advantage of polynomial
factorization and decomposition algorithms, and pattern matching.

This is an obviously limited approach and there is a need, in various areas of symbolic
mathematics, e.g. solving of systems of polynomial equations [Strzebonski1997computing]_, to
compute values of roots of a polynomial to a desired precision. This could be done by using
numerical root finding algorithms, like Durand--Kerner's, which is has its implementation
in mpmath library and is exposed to the top--level via :func:`nroots` function. However, in
pathological cases, numerical algorithms may fail to compute correct values of polynomials'
roots.

To tackle this problem, when the user needs guaranteed error bounds of the computed roots,
symbolic root isolation algorithms can be used. SymPy can isolate roots of a polynomial with
rational coefficients in real and complex domains, taking advantage of most recent algorithmic
solutions in the field. Symbolic root isolation is not that efficient as numerical root finding,
but is always successful for arbitrary polynomials, giving, as the result, isolating intervals
of the roots, in the real case, or rectangles, in the complex case.

Real roots
----------

For root isolation over reals SymPy implements continued fractions algorithm.
[Akritas2008improving]_
[Akritas2008study]_
[Sharma2007complexity]_
[Collins1976descarte]_

Complex roots
-------------

Isolation of complex roots is a much more demanding task. In SymPy we implemented the algorithm
of Collins and Krandick [Collins1992infallible]_, the best currently known algorithm for symbolic
complex root isolation (it is also implemented in Mathematica, see [Mathematica2009internal]_ for
details).

Collins--Krandick algorithm is an infallible (purely symbolic) algorithm for isolating complex
roots of univariate polynomials with rational and Gaussian rational coefficients. In SymPy we
currently allow only rational coefficients, but extension to the more general domain should be
rather straightforward (Gaussian rational domain has to be implemented).

The algorithm starts with a sufficiently large rectangle, which contains all roots the input
polynomial, it bisects this rectangle, either vertically or horizontally, depending on the
geometry of the isolation rectangle and computes the number of roots in each bisected part.
If there are no roots in a rectangle then such a rectangle is skipped. If there is exactly
one root, then the algorithm returns the rectangle a solution. Otherwise, the new rectangle
is added to a queue and scheduled for further bisection. The initial rectangle is computed
using Cauchy bound, which may give large overestimation on the magnitude of roots. If the
there are no more rectangles left, i.e. each resulting rectangle contains only a single
root (is an isolation rectangle), then the algorithm terminates. After the isolation phase,
resulting rectangles can be further refined to the desired precision.

As only rational coefficients are allowed, this gives the possibility of improving the speed
of computations by isolating strictly complex roots only in the upper half--plane, excluding
the real line (positive imaginary component). Conjugates are located by symmetry and real
roots are located using much more efficient real root isolation algorithm.

An important issue is location of roots on the boundary of an isolation rectangle. The
algorithm can easily count roots in such setup (as opposed to other complex root isolation
algorithm). However, to disambiguate the bisection scheme, where the same could be counted
as a part of two (or more) adjacent rectangles, we only count roots located on the northern
and western edges, and on the north--western corner of an isolation rectangle.

The current implementation of Collins--Krandick algorithm in SymPy is suboptimal and there
are several possible enhancements, some of listed in [Collins1992infallible]_, which ought
to make complex root isolation in SymPy much faster.

Collins--Krandick algorithm seems to be a good candidate for parallelization on multiple
processors, although the author is not aware of any work tackling this problem. An approach
would be to schedule refinement of particular isolation rectangles or clusters of rectangles
on different processors. Currently we simply maintain a queue of rectangles in order from
the smallest to the largest and refine each one--by--one on a single CPU.

Previously also we experimented with, so called, global bisection algorithm due to Wilf (see
[Wilf1978bisection]_). As its name suggests, Wilf's algorithm takes advantage of bisection
scheme and operates on rectangles, similarly to Collins--Krandick algorithm, however it uses
Sturm sequences to compute the number of roots in a rectangle and thus is very slow, because
computing polynomial remainder sequences (in particular Sturm sequences) is slow a computationally
demanding process. The other issue is that when a root is located on or even near (there is no
definition of the word *near* in this context) rectangle boundary then the algorithm has to be
restarted with an updated initial configuration. This makes global bisection algorithm fragile
and unpredictable. There are other approaches to symbolic root isolation, see for example
[Pinkert1976complex]_.

Collins--Krandick algorithm takes advantage of purely symbolic approach, thus is significantly
slower than rapidly converging numerical algorithms. However, it is possible to turn it into a
mixed symbolic--numerical algorithm, where, in certain conditions, it is possible to replace
symbolic computations with validated numerical computations, without compromising properties
of the original algorithm.

It should be obvious that real root isolation is less computationally intensive than complex
root isolation, so whenever it is known that only real (or even negative or positive) roots
are required, then the domain of computation should be appropriately limited to speed up the
computations (for a detailed discussion see [Collins1996complex]_).

