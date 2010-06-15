.. include:: ../globals.def

.. _thesis-introduction:

============
Introduction
============

Hamming [Hamming1987numerical]_, in his famous book about numerical algorithms, said that
*"The purpose of computing is insight, not numbers"*, which means that we should not blindly
acquire and process raw data, but we should also learn something from it, more importantly,
something new. Numerical computing is significant in engineering and computational sciences,
because most problems, that we encounter in real--life, do not have exact solutions, however,
they can be solved to some desired precision using numerical methods. Methods of this kind
give only data. We can plot this data, we can analyze it, we can analyze the outcome of the
computations we did. But, in any case, maybe besides those trivial and not interesting at all,
we will not learn about the nature of the studied problem. This is were exact, symbolic methods
arise, which, when used properly, can give us this insight to problems we are solving.

This is one, lets say educational reason, why engineers and scientists should be interested,
at least partially, in symbolic methods. There is, however, another much more simple reason
for this: numerical methods can simply fail to compute correct results. Properly implemented
symbolic methods do not share this issue, always giving correct answers. Although, they need
more time, then numerical methods, to find a solution.

We should, however, remember that usually only small instances of particular, interesting
problems can be solved using symbolic methods. The Optimal solution is to combine both kinds
of methods, using symbolic algorithms as long as it is feasible, for example to pre--process
equations of a problem, to make them more easily solvable numerically, and then solve them
using validated numerical methods.

Symbolic manipulation systems
=============================

Systems which implement symbolic methods are called symbolic manipulation systems, also known
as symbolic mathematics or computer algebra systems, or CAS for short. In this thesis we will
use those terms interchangeably, however, some systems are more symbolic and some are more
algebraic. First symbolic mathematics systems emerged in early 1960s as the requirement of
theoretical physics and research into artificial intelligence. Those were very basic systems,
usually implemented in Lisp programming language. Over the years more symbolic methods were
invented and the design of mathematical systems improved, giving a rise to modern systems,
amongst others Reduce, Macsyma, AXIOM and Derive, and more recent including Maple, Singular,
Mathematica, Magma, Maxima, GiNaC, and many others. For a very detailed historical insight
refer to an interview [Haigh2005interview]_ with Gaston Gonnet, a key figure in computer
algebra systems design, co--creator of Maple, a leading third--party mathematical software
on the market.

The typical design approach to most of those systems is to implement two levels of software.
On the first level, called a kernel, which is usually developed in a fast, machine oriented,
compiled programming language like Lisp, C or C++, the most commonly used, core, algorithms
are implemented. This level is not accessible to the end user, disallowing users investigate
the details of the particular implementation of mathematical algorithms. On the contrary, the
other level is usually implemented in a user--friendly programming language, which is also
used for interaction with the user. On this level advanced and configurable mathematical tools
are implemented. The language for this purpose is usually and newly invented, for a particular,
symbolic manipulation system, domain specific programming language, oriented towards ease of
expressing mathematical formulations in it. This adds a cost when learning such systems, because
one has not only to understand the system it self, its semantics and behaviour, but yet another
programming language, which will be useless outside the system. Those domain specific languages
(DSLs) are often very fancy and hard to learn.

A different approach was chosen in GiNaC a library for symbolic mathematics, which was written
in C++ programming language [Frink2001large]_. Both the kernel and mathematical libraries were
implemented in this language, so users who are familiar with C++, can more easily use it than
standalone systems, described previously. Having a library has also the benefit, that one can
easily create his own programs which simply link to a single, relatively small dynamically
linked library. GiNaC is fast, but implements only very basic symbolic algorithms. Also, C++
is not a user--friendly programming language, so it might be a barier for non--programmers.

An idea emerged to use a very interactive, simple and easy to learn programming language,
Python (http://www.python.org) and expose GiNaC functionality in it. This way we arrive
with Pynac. At first this seems a great approach because we use a very fast C++ and use
well known language, which popularity is steadily growing. The disadvantage of this approach
is that once again we arrive with two languages and the C++ core is still not easily accessible
for the users. Also writing bindings to C++ libraries in Python is not that easy (there is a
need for an intermediate programming language for this).

The pure Python approach
========================

The next step in exposing internals of a symbolic manipulation system the user, was to
write such system entirely in Python. This is how |sympy| (http://www.sympy.org) was born.
The idea was very simple: lets reinvent the wheel for the 37th time and create a library
for symbolic mathematics which will be written in pure Python. Thus, |sympy| is yet another
approach to symbolic mathematics, a library written from scratch in Python, an interactive,
interpreted, dynamically typed, general purpose programming language, which aims to become
a full--featured symbolic mathematics package while keeping the code as simple as possible
in order to be comprehensible and easily extensible. Moreover, SymPy does not depend, by
default, on any external software besides a Python interpreter program, although additional
dependencies like GMPY, Cython or Pyglet (for plotting) are optional. This way it is
straightforward to use SymPy's mathematical functionality in environments like Google App
Engine or Jython (Python in Java). It is also fairly easy for people to include SymPy in
their projects.

To give |sympy| a try, lets consider a simple session in a standard Python's interpreter.
Suppose we would like to compute the following indefinite integral:
.. math::

    \int \frac{x - \tan(x)}{\tan(x)^2 + \tan(x)} dx

and later differentiate integration result, simplify and check if the result from the
integrator was correct, by comparing to the original function. A sample session would
look as follows::

    >>> from sympy import var, tan, integrate, ratsimp

    >>> var('x')
    x

    >>> f = (x - tan(x)) / tan(x)**2 + tan(x)

    >>> integrate(f, x)
    log(1 + tan(x)**2)/2 - x/tan(x) - x**2/2

    >>> ratsimp(_.diff(x)) == f
    True

First we need to import all classes and functions that we will take advantage of in this
session. We could alternatively import everything that SymPy exports by default, by issuing
``from sympy import *``, however, this approach is not recommended if the user plans to use
SymPy in parallel with other libraries, like NumPy, in a single session. We are using a
general purpose programming language, so we need to declare all symbols that we will use.
In this case we declare one symbol ``x``, using :func:`var` function, which is clever enough
to inject ``x`` into the current namespace, saving us a little typing. From this point we can
start computing with symbolics, either by using procedural (see :func:`integrate`) or object
oriented (see :func:`diff`) styles. For users convenience, both ways are usually available,
as users may have different backgrounds and may be accustomed to different styles. The ``_``
symbol, in the last input line, stands for the previous output.

The main advantage of a library written entirely in Python, is that the user have access
to all algorithms and data structures that were implemented in |sympy|, can analyze them
or experiment with them, or even provide his own implementations. This is straightforward
even for non--programmers, because there is no need to learn machine depended details. A
lot was said in the past about educational aspects of mathematical software, mostly on the
level of solving problems with such systems [Wang1976teaching]_. However, with |sympy| we
can achieve more, because we not only can compute with it but we can see exactly how each
part of |sympy| does work and were the nicely formatted results come. Thus we see |sympy|
as a promising candidate for teaching mathematics in future.

The pure Python approach has also weaknesses. The biggest problem is efficiency of such
solution. Python is an interpreted programming language, thus it is significantly slower
compiled languages. The question arises: is it at all feasible to solve any practical
problems in |sympy|. It happens that currently we can solve only problems of very small
size, because of wrong design decisions in the past. With each release overall efficiency
of |sympy| increases, but we are still far from other mathematical software.

There are other issues with pure Python approach. Suppose we would like to enter a fraction
one over three into |sympy|. Can we simply write ``1/3`` in an interpreter? Unfortunately
not, because ``1`` and ``3`` are Python objects and division of those objects will either
give an integer (floor division) or a floating--point value (this depends on the version
of Python interpreter and its configuration). In this particular case we have to tell Python
that at least one of ``1`` and ``3`` have to be a |sympy|'s object, so we have to write
``S(1)/3``, or equivalently ``S('1/3')`` or ``Rational(1, 3)``, where ``S`` is a shorthand
for :func:`sympify` function, which converts objects and strings into SymPy's objects. In
other mathematical software that use Python, for example in Sage (http://www.sage-math.org),
this problem is resolved by using a preparser, which alters Python's semantics and allows
for automatic conversions of this kind. However, we consider using by default a preparser
as actually constructing a new language, because those tiny differences might be tricky.


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

A word on time measurement
==========================

Throughout this thesis we will measure time of various function and code blocks. For this purpose,
we use IPython's built--in timing functions: ``%time`` and ``%timeit``. In the cases where we are
only interested in approximate results to show the scale of a problem, especially when computations
take a lot of time, about half a minute or more, we will use the first variant. For precise time
measurement or/and when execution times are very small (micro-- or milliseconds) we will use the
other function, ``%timeit`` , which adaptively adjusts the number of required evaluations of a
function, to give precise and valid results. In any case we can not say anything about statistics
of such measurements, because each run is influenced but fluctuations generated by the operating
system, as we can not guarantee that for each run, there will be exactly 100% of CPU time available.
However, all timings were done with no background applications running, minimising risk of getting
invalid time measurement. We used standard functionality of IPython for doing benchmarks, to allow
the reader to follow code examples we will show in this thesis and verify them on reader's computer
(all benchmarks of this thesis were done on a single core Intel Pentium--M 1.7 GHz CPU with 1 GiB
of memory, running Gentoo Linux, with kernel 2.6 series, operating system).

Acknowledgements
================

The author would like to thank members of |sympy|'s development team for their support, in particular
Aaron Meurer and Criss Smith for their important input in discussion about the module and its internals
and for many bugfixes and patches with improvements they submitted, and Ondřej Čertík for his help in
general. The author would also like to thank the supervisor of this thesis, Krzysztof Juszczyszyn, for
his patience concerning author's work on this thesis and his enthusiasm about the project.

