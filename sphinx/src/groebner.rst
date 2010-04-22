.. _thesis-groebner:

.. |groebner| replace:: Gröbner

=================================================
Introduction to |groebner| bases and applications
=================================================

The |groebner| bases algorithm specializes to:

1. *Gauss's algorithm* for linear polynomials
2. *Euclid's algorithm* for univariate polynomials

Complexity of computing |groebner| bases
========================================

::
    GroebnerBasis[{x y^3 - 2 y z - z^2 + 13, y^2 - x^2 z + x z^2 + 3, z^2 x - y^2 x^2 + x y + y^3 + 12}]

::
    groebner([x*y**3 - 2*y*z - z**2 + 13, y**2 - x**2*z + x*z**2 + 3, z**2*x - y**2*x**2 + x*y + y**3 + 12], x, y, z)


Vertex-coloring of graphs
=========================

.. math::

    V(I)


