.. include:: ../globals.def

.. _thesis-conclusions:

===========================
Final words and conclusions
===========================

In this thesis the author tried to sum up three years of his work on computer algebra part
of |sympy|. Not everything could be added to this volume however, the author hopes that
this text gives at least basic view of what polynomials manipulation module is, what were
problem we faced at theh begining of development of this module, what we did and have it
was done. In the remainder of this chapter we will briefly describe the future of the
module and possible extensions.

Future plans
============

After three years of development and after a milestone as master's thesis is, a question
arises: is this the end? Depending on the point of view we could say that fortunatelly
or unfortunatelly (crossout unneeded) there is still a lot of work to be done to make
the module even more useful. The main concern is to make the module faster. As we shoed
in the previous section, |sympy| in some cases can already beat Maxima. However, we this
not enogh, improvements are necessary.

Polynomial arithmetics
----------------------

[Monagan2009parallel]_
[Monagan2007heaps]_
[Bernstein2008fast]_

Power series expansion
----------------------

|sympy| implements algorithms for computing limits [Gruntz1996limits]_ and power series
(Taylor and Laurent series).

When the algorithms were implemented, polynomials manipulation module was almost non--existent
so everything was implemented using slow symbolic core.

The current implementation of power series is very inefficient, because although power
series are polynomials (in the case of Laurent series up to a finite number of terms,
which number is usually much smaller than then number of Taylor terms).

It would be benefitial to use
[Zippel1976expansions]_
[Brent1978fps]_
[Brent1975series]_

Partial fraction decomposition
------------------------------

[Bronstein1993partial]_
[Wang1981partial]_

Simplification of expressions
-----------------------------

[Monagan2006modulo]_
[Pearce2001relations]_
[Moses1971simplification]_

Factorization of polynomials
----------------------------


Cylindrical algebraic decomposition
-----------------------------------

Current a big weakness of polynomials manipulation module is lack of solver for multivariate
inequalities and systems of inequalities.

Cylindrical algebraic decomposition

[Arnon1984basic]_
[Jirstrand1995cylindrical]_

CAD can be also used for efficient elimination of quantifiers from second--order logical
expressions and thus is a very useful tool in simplification of expressions and assumptions engine.

Multiple algebraic extensions
-----------------------------


[vanHoeij2002modgcd]_

Using modular techniques elsewhere
----------------------------------

[Gerhard2006modular]_

