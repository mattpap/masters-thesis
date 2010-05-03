.. include:: ../globals.def

.. _thesis-glossary:

========
Glossary
========

.. glossary::

    polynomial
        http://eom.springer.de/P/p073690.htm

    admissible ordering of monomials
        An ordering, $>$, on $\mathbb{N}^n$ is called an admissible ordering of monomials
        when it satisfies the following conditions:

        #. $>$ is a total ordering on $\mathbb{N}^n$
        #. $\alpha$, $\beta$, $\gamma$ are vectors in $\mathbb{N}^n$ and $\alpha > \beta$,
           then $\alpha + \gamma > \beta + \gamma$
        #. $\alpha >= 0$ for all $\alpha$ $\mathbb{N}^n$

    algebraic variety
        The set solutions to a system of polynomial equations.

    characteristic zero
        A property of algebraic structures. An algebraic structure is of characteristic
        zero if it has infinite number of elements. Trivial examples are the ring of
        integers or the field of rational numbers. Contrary, an algebraic structure
        can be of positive characteristic, if it has finite number of elements. Then
        the characteristic tells how many elements are in the structure. In SymPy we
        can check if a domain has zero characteristic using :attr:`has_CharacteristicZero`.

    symmetric polynomial
        A polynomial $f \in \mathbb{R}[x_1, \ldots, x_n]$, where $\mathbb{R}$ is a ring,
        is called symmetric if $\sigma(f) = f$ holds for every permutation $\sigma$ of
        the set $\{x_1, \ldots, x_n\}$. Every symmetric polynomial can be rewritten in
        terms of elementary symmetric polynomials utilizing method called symmetric
        reduction. This can can be accomplished in SymPy using :func:`symmetrize`
        function.

    elementary symmetric polynomial
        A polynomial $f \in \mathbb{R}[x_1, \ldots, x_n]$, where $\mathbb{R}$ is a ring,
        is called an elementary symmetric polynomial if $f$ is symmetric and $f$ is an
        element of the basis which generates all symmetric polynomials. The $k$--th
        elementary symmetric polynomial in $n$ variables, i.e. a polynomial of degree
        $k$, can be constructed by summing all different $k$--th degree monomials in
        $\{x_1, \ldots, x_n\}$. Elementary symmetric polynomials can be generated in
        SymPy using :func:`symmetric_poly` function.

.. TODO: http://planetmath.org/encyclopedia/SymmetricPolynomial.html
.. TODO: http://planetmath.org/encyclopedia/ElementarySymmetricPolynomial.html

