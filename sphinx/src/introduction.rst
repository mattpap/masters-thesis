.. include:: ../globals.def

.. _thesis-introduction:

============
Introduction
============

Design and implementation issues of a computer algebra in an interpreted dynamically typed programming language.

Where numerical methods fail or are incompetent, giving only local view of the problem
domain, computer algebra systems, or CAS for short, arise. Hamming [9] said, concerning
numerical computations, that *"The purpose of computing is insight, not numbers"*, meaning
that besides obtaining some raw results, which we can call data, we ought to learn something,
hopefully new, from the results we get.


[Ulmer1996kovacic]_
[Frink2001large]_
[Wang1976teaching]_


Another approach to symbolic mathematics is SymPy, which is available
from http://sympy.org.  SymPy is a library written in pure Python,
which aims to become a full-featured symbolic mathematics package
while keeping the code as simple as possible in order to be
comprehensible and easily extensible. Moreover, SymPy does not depend,
by default, on any external software besides a Python interpreter,
although additional dependencies like GMPY, Cython or Pyglet (for
plotting) are optional. This way it is straightforward to use SymPy's
mathematical functionality in environments like Google App Engine or
Jython (Python in Java). It is also fairly easy for people to include
SymPy in their projects.

SymPy can be used either as a standalone library, or inside `Sage
<http://sagemath.org/>`_ (or other similar distributions like `FEMhub
<http://femhub.org/>`_). It is also part of most of the Linux
distributions and the OS X Fink package system. There is also an
installer for Windows available.

The fundamental difference between SymPy and many other mathematical
packages is that SymPy is written from scratch in a simple,
interpreted, general purpose programming language: Python.  There is
no separation between the core and user libraries, which are usually
implemented in different programming languages, the core in a compiled
(machine oriented) one and libraries in an interpreted one. This gives
great flexibility and allows the user to experiment with every detail
of SymPy, without any need for compiling code, which leads to a much
faster development cycle.

Below we use IPython, which is a feature rich version of the standard
Python shell, equipped with syntax highlighting, auto-completion, many
*magic* functions and a rich API (for details refer to
http://ipython.scipy.org). Lets consider a simple SymPy session using
IPython::

    In [1]: from sympy import var, sin, integrate, pi

    In [2]: var('x')
    Out[2]: x

    In [3]: sin(x)
    Out[3]: sin(x)

    In [4]: sin(x).diff(x)
    Out[4]: cos(x)

    In [5]: integrate(sin(x), x)
    Out[5]: -cos(x)

    In [6]: integrate(sin(x), (x, 0, pi))
    Out[6]: 2

First we need to import all classes and functions that we will take
advantage of in this session. We could alternatively import everything
that SymPy exports by default, by issuing ``from sympy import *``;
however, this approach is not recommended if the user plans to use
SymPy in parallel with other libraries, like NumPy, in a single
session. We are using a general purpose programming language, so we
need to declare all symbols that we will use. In this case we declare
one symbol ``x``, using :func:`var` function, which is clever enough
to inject ``x`` into the current namespace, saving us a little
typing. From this point we can start computing with symbolics, either
by using procedural (see :func:`integrate`) or object oriented (see
:func:`diff`) styles. For users convenience, both ways are usually
available, as users may have different backgrounds and may be
accustomed to different styles.

For a detailed explanation of SymPy's functionality and its semantics,
refer to SymPy's documentation, which is available at
http://docs.sympy.org. If help is needed, then one may ask questions
at SymPy's mailing list sympy@googlegroups.com or IRC channel
``#sympy`` at irc.freenode.net.

The same behavior can be obtained from inside Sage. There is full
interoperability between Sage's and SymPy's functionality. For
example, the user can create Sage's expressions and use them with
SymPy's classes and functions, and then use the computed results back
in Sage. All conversions, in both directions, are done automatically.

There exists a similar link between SymPy and mpmath, a library for
arbitrary precision numerical computing in Python (see the following
section for more details). SymPy is a symbolic mathematics library,
but it also allows for numerical evaluation thanks to the mpmath
library, which is included by default in SymPy. For example, SymPy
implements a symbolic integrator and the user can compute various
classes of integrals in a purely symbolic way. It is easy to also
compute similar integrals numerically using mpmath.  The bindings are
sufficiently strong so that the user doesn't have to do any manual
conversions or even use mpmath's functionality directly, although if
needed, anything specific can be imported explicitly from mpmath.

SymPy ships with a simple script called ``isympy``, which can be used
to run SymPy as a standalone application. The script chooses the best
Python shell installed on the system (e.g., IPython, if available, and
falls back to a standard Python shell otherwise), imports SymPy,
setups pretty printing and injects some predefined symbols and
functions declarations into the current namespace, for user
convenience.

Although the project started in 2006, SymPy already implements a wide
variety of algorithms and data structures for symbolic
manipulation. SymPy can do basic arithmetic, calculus
(differentiation, integration, limits), simplification of expressions,
polynomials (factoring, expansion, Gröbner bases), pattern matching,
solving (algebraic, difference and differential equations, and systems
of equations), symbolic matrices (determinants, LU decomposition,
eigenvalues/eigenvectors), 2D and 3D plotting, Unicode pretty printing
of expressions and more. Lets consider a few nontrivial examples of
SymPy's capabilities::

    In [1]: from sympy import *

    In [2]: var('x')
    Out[2]: x

    In [3]: sqrt3 = lambda x: x**(S(1)/3)

    In [4]: limit((sqrt3(x**2) - 2*sqrt3(x) + 1)/(x - 1)**2, x, 1)
    Out[4]: 1/9

    In [5]: f = (x - tan(x)) / tan(x)**2  +  tan(x)

    In [6]: integrate(f, x)
    Out[6]: log(1 + tan(x)**2)/2 - x/tan(x) - x**2/2

    In [7]: ratsimp(diff(_, x)) == f
    Out[7]: True

This example shows one important point about SymPy and the pure Python
approach. In the third input we wrote ``S(1)/3`` to get the rational
one over three. Why couldn't we simply write ``1/3``? This is because
``1`` and ``3`` are Python objects and division of those objects will
either give an integer (floor division) or a floating--point value
(this depends on the version of Python interpreter and its
configuration). In this particular case we have to tell Python that
``1`` should be a SymPy's object, so we need to write ``S(1)``.  ``S``
is a shorthand for :func:`sympify` function, which converts objects
and strings into SymPy's objects. We could write alternatively
``S('1/3')`` or ``Rational(1, 3)``, but never ``1/3`` directly. This
is a cost associated with the approach we took when designing SymPy.
In contrast, in Sage this problem is automatically dealt with via a
preparser.

    sage: 1/3
    1/3

There is another frequently asked question concerning any library
written entirely in an interpreted programming language for the very
demanding task of symbolic manipulation: is SymPy at all efficient?
Compared to Pynac, which uses an optimized core written in C++ (a
fast, machine-oriented programming language), SymPy can be considered
slow, because of the significant overhead of interpretation of the
Python language.  In some areas SymPy can already compete with other
mathematical software, for example with Maxima when computing certain
classes of Gröbner bases. There are efforts ongoing to make SymPy
faster, e.g., by using pure mode Cython (this approach allows us to
compile Python source code, while keeping a single source base). We
are also considering writing tiny auxiliary modules in Cython for time
critical parts of SymPy.

Besides those issues, the pure Python approach seems very promising,
for example in teaching, because it allows for analysis and
modification of the implemented algorithms and data structures, on any
level, even by people with only moderate programming experience and
knowledge of Python.




   SymPy is not the first approach to the problem of designing a computer algebra
system, nor the last. First CAS emerged in early 1960s as the requirement of
theoretical physics and research into artificial intelligence. For a detailed historical
insight refer to an interview [8] with Gaston Gonnet, a key figure in computer algebra
systems design, co–creator of Maple, a leading third–party CAS. The early systems,
which provide basis for modern tools, include, amongst others, Reduce, Macsyma,
AXIOM and Derive. The more recent are Maple, Singular, Mathematica, Magma,
Maxima, Yacas, GiNaC, SAGE etc.

    The standard approach [10] to computer algebra systems design was to separate the
system into a core (engine) and a mathematical library. The core was written in
a higher–level, compiled (to machine code) programming language, like Lisp, C or
C + +, and implemented low–level primitives, resource demanding algorithms, but
also, a compiler (to machine independent byte code) of a new extension (domain
specific) language, or DSL for short, and its evaluator (virtual machine). The
mathematical library implemented actual algorithms, transformation rules etc., using
the newly invented language.
    In our view this approach is unfortunate, because it implies additional burden of
setting up whole grammar, parsing mechanisms, evaluation etc. of the new DSL and
requires users to learn this new language to use the system. The situation gets even
worse when there are several computer algebra systems that each specialize in
different fields of science and each having its own scripting language, usually with
many subtle differences from others (e.g. operator precedence). Most notable
exceptions to this rule are GiNaC and SAGE.
    GiNaC is a C + + library designed to allow the creation of integrated systems that
embed symbolic manipulations together with more established areas of computer
science, like computation–intense numeric applications, graphical interfaces, etc.,
under one roof [2]. Although GiNaC does not introduce a new a new domain specific
language, it is a very inefficient practice to script GiNaC directly in C + +, due to its
non--dynamic characteristic and lack of interactiveness (compilation required).
    To overcome this difficulty several Python based interfaces were developed. The
most notable implementations are pyginac and swiginac. Although both allow its users
to access GiNaC features from an interactive environment, still all modifications of
the core of GiNaC are needed to be written in C + +.
    SAGE [15] goes a step further and provides a coherent interface, written in Python
and Cython (a static compiled to C version of Python), to several computer algebra
systems and scientific libraries in the market, both open source and third--party. Note
that SymPy is included in SAGE as a part of the distribution. SAGE also provides
many additional features like interactive web notebooks, similar to Mathematica's
notebook but much more powerful. However the preferred way to work with SAGE is
using a preparser of a Python--like language.
    Combining best features of many existing systems, which are being considered as
leaders in their fields of expertise, in a single environment seems very appealing, as
user is no more required to learn the language of choice of each single system that
SAGE maps to, and each system incorporates its optimum of computing power in its
field. This gives an impressive tool for doing both numeric and symbolic
computations.
    There are however deficiencies of this model. SAGE itself can not be called an
algebra system but rather a software distribution, very large in size, as all subsystems
are included in appropriate versions to build APIs. Being built as a glue to bind
together heterogeneous subsystems, if there is a bug in one of those systems, one has
to be an expert in that subsystem, or otherwise it's difficult to fix the bug. As opposed
to a homogeneous system, written just in Python and possibly Cython.

What is symbolic manipulation?
==============================


And what is computer algebra?
=============================

The state of art in symbolic and algebraic computing
====================================================

There is another term often used when speaking about symbolic manipulation


What is a polynomial?
=====================

Polynomials at the core of this thesis and it would be very unwise to proceed with any discussion about
the internals of polynomials manipulation module without giving a definition of this fundamental concept.
Suppose we are given an expression $7*x**3 + x*y + 11$. Is it a polynomial? A high school student can
answer this question affirmatively: yes, this is a polynomial.

But it this all? Hopfully not, because
if we recognize the expression as a polynomial we can take advantage of this fact.


The current version
===================

Polynomials manipulation module is under continuous development, so the notion of, so called, current
version of the module, which was used for writing this thesis, was a fluid concept and changed as this
thesis was being written. As of the finalization of this thesis, the current version was the HEAD of
branch *polys9* in development repository of the author, located at http://github.com/mattpap/sympy-polys.
All stable results of this branch were already merged with *master* branch of official repository of
|sympy| and are scheduled for release with the upcoming 0.7.0 release of |sympy|.

Origin of module's name
=======================

For most people, it would be more straightforward to name the module simply *polynomials*, instead
of the shorter name *polys*, which is currently in use. There are two reasons for having the latter
in |sympy|. The first reason is that the name *polys* is just shorter and, this way, it is easier to
use it in interactive sessions. Polynomials manipulation module has a very rich API, which makes it
necessary, in some cases, to explicitly abbreviate function and class names with the module name.
Alternatively, we could use module name aliases, but this would lead to inconsistent naming scheme
and confusion for inexperienced |sympy|'s users. The other reason is less trivial and has historical
background. The first module for polynomial manipulation was developed during Google Summer of Code
2007, and later, when a new module was under implementation, for a year there were to modules for
polynomials manipulation in parallel, so a different name was necessary. Afterwards, the new name,
*polys*, was kept, see next section for a more detailed discussion.

Historical background
=====================

At the very beginning, in 2006, |sympy| was lacking a separate module for polynomial manipulation.
This was not a pity, because a well established module of this kind was necessary for making |sympy|
grow and work on algorithms that depend on polynomials was a big struggle. A task for implementing
polynomials in |sympy| was proposed by a German student for Google Summer of Code 2007. The student
was selected for the task and developed a basic module during GSoC time frame. The module was called
*polynomials* and featured elementary polynomial arithmetics, real root counting and root finding via
radicals, GCD and LCM algorithms, square--free decomposition, univariate and multivariate factoring
into irreducibles over rationals (Kronecker's algorithms) and |groebner| bases. Later the module was
extended with fast modular factorization algorithm in the case of univariate polynomials. This was,
unfortunately, last development in SymPy by the original author. For several months polynomials
manipulation module was not maintained.

The same year, in 2007, the author of this thesis was selected within Google Summer of Code for
implementing, so called, *concrete mathematics* module in |sympy| [Graham1994concrete]_. At that
time, the author was interested in automated methods for solving discrete problems, especially
those involving recurrence relations [Nemes1997monthly]_. The task was to extend |sympy| with
algorithms for finding closed forms of symbolic summations and solving recurrence relations
[Petkovsek1997AeqB]_, [Abramov1995rational]_, [Petkovsek1992hyper]_. Although the preliminary
developments were possible without direct usage of polynomials manipulation algorithms, later
on the barrier between the two modules was shrinking very rapidly as new algorithms were scheduled
for implementation in concrete mathematics module. The author was required several times to implement
polynomials manipulation related tools on his own. Altogether, it was a great experience for the
author, showing him the importance of polynomials and related algorithms in a symbolic manipulation
system, not only as a standalone tool, but also as a component of other, often very complex, algorithms.

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
1.0.0 of |sympy|, significant changes to the API may still occur.

Presentations of this work
==========================

Early results concerning polynomials manipulation module were presented at students conference in
2009 [KNS2009]_, which was held at University of Technology in Wrocław, Poland. A more extensive
talk (including a short tutorial) was given by the author of this thesis the same year at EuroSciPy
conference [EuroSciPy2009]_, which was held in Leipzig, Germany. This was a general presentation
about |sympy| with some remarks concerning polynomials manipulation in pure Python. In 2010, at Python
for Scientists (py4science) meeting, the author had a talk and a tutorial [Py4Science2010]_ dedicated
to polynomials manipulation. The event took place at University of California at Berkeley, CA, USA. In
the presentation the author showed intermediate results of his work on polynomials manipulation module
and of this thesis. For July 2010, the author has a talk scheduled at EuroSciPy conference [EuroSciPy2010]_,
which will be held this time at Ecole Normale Supérieure in Paris, France. Final results will be presented
during this talk.

The structure of this thesis
============================

In this chapter we gave a brief introduction to SymPy and symbolic and algebraic computing in general.
More importantly, we also described author's input to SymPy and defined the goals of this thesis. In
the following chapters, in three, hopefully not too overlong, steps, we will discuss the issues that
were pointed out in this chapter and how we solved them. Thus, in the next chapter we will discuss
the details of the internal implementation of polynomials manipulation module, i.e. the heart of the
module. In the third chapter we will briefly describe algorithms that where implemented in the module,
giving many references to important literature. In the fourth chapter we will show that polynomials
manipulation module can be employed for solving practical problems. This chapter will introduce the
reader, in a tutorial like fashion, to the theory of |groebner| bases and will examine several
interesting examples. In the final chapter we will sum up all what was said about computer algebra
in pure Python and discuss future plans for the module.

Acknowledgements
================

The author would like to thank members of |sympy|'s development team for their support, in particular
Aaron Meuer and Criss Smith for their important input in discussion about the module and its internals
and for many bugfixes and patches with improvements they submitted, and Ondřej Čertík for his help in
general. The author would also like to thank the supervisor of this thesis, Krzysztof Juszczyszyn, for
his patience concerning author's work on this thesis and his enthusiasm about the project.

