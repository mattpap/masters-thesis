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

Euclidean algorithms
====================

GCDs and LCMs
=============

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

Real roots
----------

Complex roots
-------------

    Implemented Collins-Krandick root isolation algorithm

    Based on the infallible algorithm for counting roots in a
    rectangle in the complex plane, an algorithm for isolation
    of complex roots of polynomials with rational coefficients
    was implemented.

    The algorithm computes the number of roots in a sufficiently
    large initial rectangle (using Cauchy bound) and then performs
    vertical and horizontal bisections and root counting until only
    rectangles with exactly one root in each remain.

    The algorithm isolates roots only in the upper half plane, but
    excluding the real line, so real roots of the input polynomial
    are discarded immediately and can be isolated using much more
    efficient continued fraction approach. Conjugates are trivially
    added to the resulting rectangles list by symmetry.

    The problem of roots located on boundary of isolating rectangles
    is resolved by counting only roots that are located on northern
    and western edges, and on north-western corner. This implies
    the fact that the real line is not considered for root counting
    at all.

    Isolating rectangles are sorted by their real component and
    then by negated imaginary component, so that root and its
    conjugate are located together forming a pair.

    This is not the optimal implementation of Collins-Krandick
    algorithms and several significant improvements are possible.

