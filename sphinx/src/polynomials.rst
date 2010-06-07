.. include:: ../globals.def

.. _thesis-polynomials:

=======================================
Polynomials over Various Ground Domains
=======================================

In the two previous chapters we introduced the reader to the internals of polynomials manipulation
module in |sympy| and described algorithms that were implemented. The discussion was grounded on a
very detailed and technical level. In this chapter we will move to a much more practical level and
show how to use polynomials in |sympy| for something useful. We will be mostly concerned about the
public API and behaviour of polynomial manipulation tools over different ground domains.

We will start our discussion from the two simplest but also the most common cases, polynomials over
the ring of integers and the rational field, and later proceed to more complex domains. Although
integers and rationals form the simplest domains, they are ubiquitous in polynomial manipulation
and polynomial over many other domains can (or have to) be transformed into one of those domains.
For example, if |sympy| encounters a polynomial with coefficients from a polynomial ring, then
when computing a factorization of such a polynomial, |sympy| will transform it to form a polynomial
over the ring of integers, factor the resulting polynomial and transform the factors back to the
original domain.

The simple domains
==================

To cons




Finite Fields
=============


Symmetric and non--symmetric representation
===========================================

Consider a finite field $\F_k$ with $k >= 2$ elements. The symmetric representation of $\F_k$
is the set of integers $\{ -\floor{\frac{k}{2}}, \ldots, \floor{\frac{k}{2}} \}$. Contrary,
the non--symmetric representation of this finite fields is the set of integers $\{ 0, \ldots,
k-1 \}$.

Internally in the polynomials manipulation module, all computations over finite fields are done
using the non--symmetric representation, which is the *natural* approach in this case. However,
the question is how to represent a polynomial which is a result from conversion from a polynomial
over a finite field to a polynomial over the ring of integers. |sympy| gives two options here. We
can either keep the non--symmetric representation or convert to the symmetric representation. The
later is the default, because it is much more natural to compute with symmetric coefficients and
usually this is the only choice which guarantees correct results (e.g. during Hensel lifting).

To keep the non--symmetric representation during conversion, one has to set ``symmetric`` keyword
argument to ``False``. This will affect only a single computation or a particular polynomial, until
the information is lost (e.g. by converting to an expression). Note that setting this arguments also
affects the way polynomials over finite fields are printed. The user can achieve the same goal by
changing global settings via a context manager or configuration utility of the module.

Suppose we have a polynomial $x^11 + x + 1$ over a finite filed $\F_{65537}$. We will factor $f$
and then expand the resulting factorization using both representations of finite fields::

    >>> factor(x**11 + x + 1, modulus=65537)
    ⎛ 2        ⎞ ⎛ 9    8    6    5    3    2    ⎞
    ⎝x  + x + 1⎠⋅⎝x  - x  + x  - x  + x  - x  + 1⎠

    >>> expand(_)
     11
    x   + x + 1

    >>> factor(x**11 + x + 1, modulus=65537, symmetric=False)
    ⎛ 2        ⎞ ⎛ 9          8    6          5    3          2    ⎞
    ⎝x  + x + 1⎠⋅⎝x  + 65536⋅x  + x  + 65536⋅x  + x  + 65536⋅x  + 1⎠

    >>> trunc(expand(_), 65537)
     11
    x   + x + 1

In the first case, we obtained both positive and negative coefficients, and it was straightforward
to expand the factorization. In the later case, where we used non--symmetric representation, we got
only positive (large) coefficients, which after expansion result in a different polynomial than the
one we obtained in the former case. To get the same result, we need to truncate coefficients of the
expanded polynomial modulo $65537$.


Conclusion
==========

In this chapter we showed how to actually use polynomial manipulation module in practise. This
tutorial like introduction might have been useful to grasp some of the ideas described in detail
in the previous, more technical, chapters. It might seem like a little abuse to add a chapter of
this kind to this thesis, however, design of an API that is comfortable to the users is one of
the main objectives of this work. In the following chapter we will say more practical use--cases
of this module on the  ...


