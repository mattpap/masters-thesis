.. include:: ../globals.def

.. _thesis-introduction:

============
Introduction
============

What is symbolic manipulation?
==============================

The current version
===================

Polynomials manipulation module is under continuous development, so the notion of, so called, current
version of the module, which was used for writing this thesis, is a fluid concept and changed during
as the thesis was being written. In general, as the current version we can understand the HEAD of the
``polysn`` branch, where ``n`` is a positive integer, currently ``n = 9``, of git development repository
of the author: ``http://github.com/mattpap/sympy-polys``.

Origin of the name *polys*
==========================

For most people, it would be more straightforward to name the module simply *polynomials*, instead
of the shorter name *polys*, which is currently in use. There are two reasons for having the latter
in |sympy|. The first reason is that the name *polys* is just shorter and, this way, it is easier to
use it in interactive sessions. Polynomials manipulation module has a very rich API, which makes it
necessary, in some cases, to explicitly abbreviate function and class names with the module name.
Alternatively, we could use module name aliases, but this would lead to inconsistent naming scheme
and confusion for inexperienced |sympy|'s users. The other reason is less trivial and has historical
background. The first module for polynomial manipulation was developed during Google Summer of Code
2007 and later, when a new module was under implementation, for a year there were to modules for
polynomials manipulation in parallel, so a different name was necessary. Afterwards, the new name,
*polys*, was kept.

Historical background
=====================

At the very beginning, in 2006, |sympy| was lacking a separate module for polynomial manipulation.
This wasn't a pity, because a well established module of this kind was necessary for making |sympy|
grow and implementation of algorithms that depend on polynomials was a big struggle. A task for
implementing polynomials in |sympy| was proposed by a German student for Google Summer of Code 2007.
The student was selected for the task and developed a basic module during GSoC time frame. The module
was called *polynomials* and featured elementary polynomial arithmetics, real root counting and root
finding via radicals, GCD and LCM algorithms, square--free decomposition, univariate and multivariate
factorization into irreducibles over rationals (Kronecker algorithms) and |groebner| bases. Later the
module was extended with fast modular factorization algorithm of univariate polynomials. This was,
unfortunately, last development in SymPy of the original author. For several months polynomials
manipulation module wasn't maintained.

The same year, in 2007, the author of this thesis was selected within Google Summer of Code for
implementing, so called, *concrete mathematics* module in |sympy|. The task was to extend |sympy|
with algorithms for finding closed forms of symbolic summations and solving recurrence relations.
Although the preliminary developments were possible without direct usage of polynomial manipulation
algorithms, later on the barrier between the two modules was shrinking very rapidly as new algorithms
were scheduled for implementation in concrete mathematics module. The author was required several
times to implement polynomial manipulation related tools on his own. Altogether it was a great
experience for the author, showing importance of polynomials and related algorithms, not only as
a standalone tool, but also as a component of other, often very complex, algorithms.

It was a natural thing to takeover polynomials manipulation module after departure of its original
author. At first the plan was just to maintain the existing code and improve speed of the module in
a few places (e.g. implement better polynomial arithmetics). However, as |sympy| grown the need for
more general and faster polynomial manipulation tools was also growing. The author soon realised that
the original module didn't provide a sufficiently strong basis for new developments in this area. The
decision was to implement a new module for polynomials manipulation in parallel with the existing one
and reusing as much code as possible from the *polynomials* module. By reusing we mean taking most
algorithms to assure correctness. During later stages of development some of the original algorithms
were replaced with more general or faster ones.  Many bugs in the original code were revealed and fixed.
Work on the new module was carried through 2008. During that time, |sympy| had two modules for polynomials
manipulation. To avoid confusion, the new module was named *polys* and other modules were gradually
refactored to use the new implementation.  At the end of 2008 the old module was removed and *polys*
remained the main and the only module for polynomials manipulation. The name *polys* was kept, because
of its short length, which is beneficial when experimenting with polynomials in interactive sessions.

At that time, although the new module was a big step forward, the author realised that its design is
still very limited and requires deep changes to make it an even better basis for future developments
in |sympy|, that require strong support for polynomials. The first few new developments were done on
top of *polys* module and preliminary results were presented during EuroSciPy 2009 conference. After
the conference, in two months, a completely new structure of polynomials manipulation module was
implemented which superseded the old design. All developments were done this time gradually on the
existing module, however, the scale of changes soon gave a rise to a completely new module, which
is the main actor of this thesis. To keep continuity in the naming convention, the name *polys*
remained and there are no plans, in foreseeable future, to return to the original name.

Hopefully, as the author predicts, this was the last major rewrite of polynomials manipulation module.
The new structure allows to rewrite parts of the module, introducing better quality, without touching
other parts. Also the public API seems to be quite stable at this point, however, till major version
1.0.0 of |sympy| significant changes to the API may still occur.

Presentations of this work
==========================

Early results concerning polynomials manipulation module were presented at Students Conference in 2009,
which was held at University of Technology in Wrocław, Poland (see [KNS2009]_). A more extensive talk
(including a short tutorial) was given by the author at EuroSciPy conference in 2009, which was held in
Leipzig, Germany (see [EuroSciPy2009]_). This was a general presentation about |sympy| with some remarks
concerning polynomials manipulation. In 2010, at Python for Scientists (py4science) meeting, the author
had a talk and a tutorial dedicated to polynomials manipulation. The event took place at University of
California at Berkeley, CA, USA (see [py4science2010]_). In the presentation the author showed preliminary
results of his work on polynomials manipulation module and of this thesis. For July 2010, the author has
a talk scheduled at EuroSciPy conference, which will be held at Ecole Normale Supérieure in Paris, France
(see [EuroSciPy2010]_).

