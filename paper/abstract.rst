
Polynomial Manipulation in SymPy (or making pure Python fast and beyond ...)
============================================================================

Computations with polynomials are at the core of computer algebra and
having a fast and robust polynomials manipulation module is a key for
building a powerful symbolic manipulation system.

Previously SymPy had extensive support for manipulation of symbolic
expressions and only very limited utilities for algebraic computations,
specifically computations in polynomial algebras. This was a significant
practical limitation when implementing the classical toolbox of symbolic
manipulation systems, which includes symbolic integration and summation
algorithms, exact solvers and many others.

The new module for polynomial manipulation implements vast majority of
algorithms related to the field, ranging from simple tools like polynomial
arithmetics, to advanced concepts including Gröbner bases and multivariate
factorization over algebraic number domains.

In this article we will show step by step how the polynomials manipulation
module was designed and implemented, and what issues aroused during its
development. Specifically we will focus on the problem of making pure
Python implementation of this module fast and discuss possible future
improvements both on pure Python level and beyond that, for example by
using pure mode Cython.

We will also show a practical example of using the new module and compare
it with popular symbolic manipulation systems on the market, which includes
Mathematica, Maxima and AXIOM.

