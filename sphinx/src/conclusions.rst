.. include:: ../globals.def

.. _thesis-conclusions:

===========================
Final words and conclusions
===========================

In this thesis the author summed up three years of his work on computer algebra module for
|sympy|, a library for symbolic mathematics in pure Python. We showed the state of art in
symbolic and algebraic computing, and described SymPy and its goals as a side effect. We
also introduced polynomials manipulation module, which was the central part of this thesis.
In three chapters we described the internal design and algorithms of the module, and showed
some practical examples of its applications. Not everything could have be written in this
volume, due to its limited capacity, however, the author hopes that this text have given
at least basic insight into what symbolic and algebraic computing in pure Python is. Time
and users' interest (or not) in |sympy| and its polynomials manipulation module, will show
if it was the right decision to design and implement such software from scratch, in an
interpreted, dynamically typed programming language. In the remainder of this chapter we
will briefly describe the future of the module and possible further developments.

Future plans
============

After three years of development and, especially, after such an important milestone as master's
thesis is, a question arises: is this the end? Or, if this is not an end, how much work is still
in front of us? In this thesis we already often speculated about future developments that could,
or better should, be done to improve polynomials manipulation module. In the field of symbolic
and algebraic computing, tree years are not enough to catch up with other software that is on
the market for 20, 30 or even 40 years. We hope that |sympy| and its computer algebra module
will steadily grow and more cutting edge algorithms will be implemented in it. To point out
some of the future ways in which the module might be heading, we devote the rest of this section
to list some ideas for future development. This is obviously and more ideas can be found in
the source code, documentation and |sympy|'s web pages, especially those concerning Google
Summer of Code program.

Polynomial arithmetics
----------------------

We already said quite a lot about arithmetics of polynomials, also about possible improvements
in this area. Improvements that are commonly known the many people, not necessarily interested
very much in computer algebra. However, there are other, less familiar algorithms for doing
polynomial arithmetics, especially of large sparse multivariate polynomials, which are not
limited to integer or rational domains. A nice example are algorithms for polynomial multiplication
and division based on heaps [Monagan2007heaps]_. Experimental data reveals that this is currently
the best approach to compute with sparse polynomials in many variables (which is actually the
most important case when computing with polynomials). The algorithm can also be relatively
easily parallelized, see [Monagan2009parallel]_ for detailed discussion.

Power series expansion
----------------------

|sympy| implements a very modern algorithm of Gruntz for computing limits symbolically [Gruntz1996limits]_,
thus, as a side effect, |sympy| is quite comprehensible in computing truncated power series of elementary
and special functions (Taylor and Laurent series). When the algorithms for those two tasks were implemented,
polynomials manipulation module was almost non--existent, so everything was implemented using slow symbolic
core. This makes any computations concerning limits and power series very slow, because the underlying
algorithms are implemented in an inefficient way. Many benchmarks show that |sympy| can be enormously slow
when computing series expansions of composite functions or when many terms are requested.

It would be beneficial to improve this picture by employing efficient polynomials manipulation algorithms
whenever possible, when computing limits and power series. Additional algorithms would have to be added
to the module, to allow efficient compositions and reversions of power series [Zippel1976expansions]_,
[Brent1975series]_, [Brent1978fps]_. This would be very advantageous for |sympy|, because limits and
truncated power series are ubiquitous in other algorithms of symbolic mathematics and are also very
useful as standalone tools in many practical problems.

Partial fraction decomposition
------------------------------

Decomposition algorithms of rational functions into partial fractions are also very useful tools
in symbolic mathematics. In |sympy| we currently implement an algorithm of Manuel Bronstein
[Bronstein1993partial]_, which allows to compute full partial fraction decompositions purely
formally, without introducing algebraic numbers. This is a spectacular approach, but also a
quite inefficient one. It would be beneficial to incorporate modular techniques into partial
fraction decomposition algorithms, for example using methods of [Wang1981partial]_. This would
allow computations of partial fractions efficiently whenever possible and Bronstein's algorithm
would be used as a fallback.

Simplification of expressions
-----------------------------

Polynomial manipulation algorithms have a natural area of application, which is simplification
of expressions [Moses1971simplification]_. Currently we already employ algorithms related to
polynomials for this task, but we do not utilize their full potential in this case. Expression
simplification is ubiquitous in symbolic mathematics systems, thus it must be general on hand but
also very efficient on the other. One very interesting case is simplification of rational functions
with polynomial side relations (modulo polynomial ideals), which was already studied in detail in
literature [Pearce2001relations]_, [Monagan2006modulo]_. This kind of simplification would allow
the user to compute efficiently with expressions like trigonometric polynomials, which are an
important tool in geometry and robotics.

Cylindrical algebraic decomposition
-----------------------------------

Currently one of big weaknesses of polynomials manipulation module is lack of solvers for multivariate
polynomial inequalities and systems of polynomial inequalities. |sympy| can solve many kinds of problems
related to polynomial equations and systems of polynomial equations, thanks to the |groebner| bases
method. It can also handle univariate inequalities via root isolation. However, multivariate inequalities,
especially over reals, are currently a no--go for |sympy|. The real case is very important, because it is
related to the problem of quantifier elimination and theorem proving in algebraic geometry.

A tool that is needed to allow |sympy| for handling multivariate inequalities is cylindrical algebraic
decomposition [Arnon1984basic]_, [Jirstrand1995cylindrical]_, or CAD for short. Given a multivariate
polynomial inequality or system of inequalities, CAD decomposes those inequalities to form a system
of inequalities that are easier to reason about. This has many applications in, already mentioned,
quantifier elimination and algebraic geometry, but also when evaluating multiple integrals and in
assumptions engine.

Multiple algebraic extensions
-----------------------------

In section :ref:`thesis-algebraic` we said that |sympy| currently requires to compute a primitive
element of a field extension if multiple extensions are provided, when computing with algebraic
numbers. We also gave references to articles concerning polynomial factoring algorithms, which
can work directly with multiple extensions. There are, however, algorithms for other areas of
symbolic mathematics, for example for computing GCDs of polynomials [vanHoeij2002modgcd]_, that
also do not require primitive element computations. Although, it is uncertain if those algorithms
are truly advantageous, it might be still worthwhile to experiment with them.

Using modular techniques elsewhere
----------------------------------

Work on polynomials manipulation module revealed that, so called, modular or p--adic techniques
[Yun1976padic]_, give very encouraging results when concerned about speed of computations. Many
classes of algorithms already benefit from this in |sympy|, most notable are factorization and
resultant algorithms, and other, like polynomial GCD algorithms, will be in future implemented.

Following this success, we should incorporate modular techniques outside polynomials manipulation
module. We already pointed out a method for computing partial fraction decomposition, but there
are other areas where those methods are applicable. A good examples are algorithms for symbolic
summation and integration [Gerhard2006modular]_. Modular method limit the range of application
of algorithms to integers and rationals, but those are the most commonly used domains in |sympy|,
so the hassle is definitely worthwhile.

