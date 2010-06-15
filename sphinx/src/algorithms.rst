.. include:: ../globals.def

.. _thesis-algorithms:

=====================================
Algorithms for algebraic computations
=====================================

|sympy| implements a wide variety of algorithms for polynomials manipulation, which ranges from
relatively simple algorithms for doing arithmetics of polynomials, to advanced methods for
factoring polynomials into irreducibles over algebraic number fields or computing |groebner|
bases. In this chapter we will shortly describe most important algorithms of polynomials
manipulation module in |sympy|. The descriptions will include a brief note on the purpose and
applications of a particular algorithm. Where possible, we will also discuss computational
complexity of an algorithm and possibility for parallelization.

We will also give references to the most influential literature (papers, books, proceedings, etc.)
about every algorithm that will be described in this study. Besides theses bibliographical items,
during development of polynomials manipulation module, we also used several classical books on the
topic of symbolic and algebraic computing: [Davenport1988systems]_, [Geddes1992algorithms]_,
[Gathen1999modern]_ and [Grabmeier2003algebra]_, to name a few, which are considered to be the
main source of knowledge on algorithms and data structures in this field. We also took advantage
of Donald Knuth's famous books, especially the volume concerning semi--numerical algorithms
[Knuth1985seminumerical]_. We also used general books on algorithms and data structures, like
[Cormen2001algorithms]_, and mathematical tables, e.g [Abramowitz1964handbook]_ (which was very
useful when implementing special polynomials, e.g. orthogonal polynomials).

Arithmetics of polynomials
==========================

Arithmetics, i.e. addition, subtraction, multiplication, exponentiation and division, of polynomials
form a basis for all other polynomials manipulation algorithms. In |sympy| we currently implement only,
so called, *classical algorithms* for this purpose, i.e. repeated squaring algorithm for exponentiation,
and $O(n^2)$ algorithms for multiplication and division, where $n$ is the maximal number of terms in
the set of input polynomials. Over finite fields we use algorithms of [Monagan1993inplace]_, which
slightly improve speed of computations over this very specific domain.

An alternative to classical algorithms are, so called, *fast algorithms*, which are sub--quadratic
time algorithms for doing arithmetics polynomials [Moenck1976practical]_. Fast algorithms are usually
limited to specific domains of computation, like integers or rationals. The family includes Karatsuba's
and FFT (Fast Fourier Transform) algorithms. The decision was made to use classical algorithms at this
point, because it is not a trivial task to make fast algorithms really advantageous, especially for
small or ill conditioned polynomials. In future, when the module will stabilize, we will consider
implementing fast algorithms, as a companion to classical algorithms, and use them where it makes
sense.

There are other ideas to improve arithmetics of polynomials, especially over integers and rationals.
An interesting example of such optimisation is algorithm of [Fateman2005encoding]_, where polynomials
with integer coefficients are encoded as sufficiently large integers and arithmetics are done using
long integer arithmetics, and later results are converted back to polynomials. This is possible by
using an isomorphism (a reversible transformation) between polynomials and integers. To make this
algorithm efficient, we need a very fast integer arithmetics library, like gmpy, which is not always
available on the system. One has to also be aware of the fact that transformations back and forth
may be very costly, especially for large polynomials.

Evaluation of polynomials
=========================

In |sympy| we employ Horner scheme [Geddes1992algorithms]_ for evaluation of univariate polynomials
over arbitrary domains. The algorithm of Horner was proved to be the optimal method for evaluation
of polynomials, which takes minimum number of additions and multiplications necessary to compute
a result. In the multivariate case, Horner scheme is non--unique, thus there are many different
schemes possible, which lead to different evaluation times. Currently we use a *natural* scheme,
which is a consequence of using by default recursive polynomial representation. In the past we
experimented with greedy algorithms for optimizing multivariate Horner scheme [Ceberio2004greedy]_,
however, without much success. This was because, although evaluation was considerably faster comparing
to the standard scheme, however optimisation times were often comparable to computation times. In future
we may reconsider using some sort of optimisation of polynomial evaluation algorithm in the multivariate
case.

Horner scheme is a very general algorithm, which is also used in |sympy| for computing compositions
and rational transformations of polynomials, and many other, which require some sort of efficient
evaluation of polynomials.

The Greatest Common Divisor
===========================

Another fundamental algorithm of polynomials manipulation is the GCD (Greatest Common Divisor)
algorithm, which allows us to compute common factors of two or more polynomials. This is very
useful on its own and as a component of other algorithms, e.g. square--free decomposition or
simplification of rational expressions.

We implement three algorithms for computing GCDs. The most general algorithm is based on
subresultants (a special case of polynomial remainder sequences) and can be used regardless
of the ground domain and polynomial representation. This is also the slowest algorithm, but
very useful if other algorithms fail or are not applicable. Where possible, we use heuristic
GCD algorithm [Liao1995heuristic]_, which transforms a problem of computing GCD of polynomials
to integer GCD problem. Although the algorithm is heuristic, with current parametrization it
never failed in |sympy|. Daily practice shows that this approach is superior to the algorithm
based on subresultants, however heuristic GCD is only limited to integers and rationals (by
clearing denominators). It also requires very efficient integer GCD algorithm, so it is
beneficial to use gmpy library for this purpose. We also implement an algorithm that uses
|groebner| bases for computing GCD of multivariate polynomials [Cox1997ideals]_. This was
historically the first implementation of multivariate polynomial GCD algorithm in |sympy|
(see section :ref:`thesis-euclid` for details).

In future we plan to implement EEZ--GCD algorithm of Wang [Wang1980eezgcd]_, [Moses1973ezgcd]_,
which we hope will improve computation of GCDs of sparse multivariate polynomials over integers
and rationals. Implementation of EEZ--GCD algorithm should be rather straightforward, because
we already have EEZ polynomial factorization algorithm implemented, and both algorithms share
a common core (variable--by--variable Hensel lifting algorithm), and they differ mainly in the
initialization phase. Having a fast algorithm for sparse polynomials is very important, because
most polynomials that we encounter in real life problems are sparse.

An alternative would be to implement sparse modular algorithm (SPMOD) of Zippel, which is also
optimized for sparse multivariate case. This algorithm is even more interesting in the light
of recent developments [Monagan2004algebraic]_, [Javadi2007spmod]_, where the algorithm was
successfully employed over algebraic number and function fields. Although there is a simple
idea standing behind SPMOD, this algorithm is considered, in the literature, to be very hard
to implement, because there are many special cases, which have to properly worked out. Thus,
at least for optimizing GCD computations over integers and rationals, we see EEZ algorithm
more beneficial at the moment.

Some parts of modular algorithms can be relatively easily parallelized on multiple processors,
because it often happens that several computations over a smaller domain have to be performed
to compute the GCD in the original domain. For example this is the case in EEZ--GCD algorithm
where, as one of initialization steps, we need to compute several univariate GCDs to compute
the original multivariate GCD. Those univariate GCDs can be very costly, but we have to do
several such computations (at least three) to guarantee correctness of EEZ algorithm (otherwise
the algorithm may fail and would have to be restarted and another sequence of univariate
polynomial GCDs would have to be computed). Those univariate GCDs can be computed in parallel,
greatly improving speed of multivariate GCD algorithm.

Square--free decomposition
==========================

Given a polynomial $f$, square--free decomposition (factorization) of $f$ gives a list of
polynomials (factors) $f_1$, $f_2$, $\ldots$, $f_n$, such that all pairs of polynomials
$(f_i, f_j)$, for $i \not= j$, are co--prime, and $f = f_1 f_2^2 \ldots f_n^n$. Thus each
$f_i$ has no repeated roots. Note that square--free decomposition does not give a true
factorization into irreducibles, although is a very important step in any factorization
algorithm (which we will describe in the following section).

In |sympy| we implement the fast algorithm of Yun [Yun1976squarefree]_ for computing square--free
decompositions in domains of characteristic zero. The cost of computing square--free decomposition
is equivalent to the computation of the greatest common divisor of $f$ and its derivative. Over
finite fields we currently use less efficient algorithm, due to odd but well known behaviour of
derivatives over domains with finite number of elements, where $f'$ might vanish even if $f$ is
non--constant polynomial (e.g. $f = x^k$ over $\F_k$, for any $k >= 2$), which leads to complications
in the algorithm. In future we should implement Yun's algorithm also in this case as well.

Factorization of polynomials
============================

Algorithms for computing factorizations of polynomials into irreducibles over various domains
are the landmark of symbolic mathematics. The work in this area started early, in ninetieth
century, and algorithms for factoring of univariate and multivariate polynomials over rationals
were invented by Kronecker. Those algorithms had exponential time complexity and were impractical
for any real--life computations. Kronecker's algorithms were the first polynomial factorization
algorithms that were implemented in |sympy|.

Over the years mathematicians tried to invent a more efficient method for factoring large polynomials,
focusing their research on univariate polynomials with integer coefficients. A partial breakthrough
came with Hensel's lemma (Hensel lifting algorithm), which allowed to perform computations with integer
valued polynomials over finite fields. Thus, an integer polynomial problem can be transformed into
finite field polynomial problem, then computations can be done in a much smaller (finite) domain and
results can be transformed (lifted) back to the integer polynomial domain.

In 1967, Berlekamp gave first complete factorization algorithm over finite fields. Moreover, this
algorithm had polynomial time complexity. Soon after, Zassenhaus combined Berlekamp's algorithm and
Hensel's lemma, giving first efficient algorithm for polynomial factorization over integers. Although,
the algorithm of Zassenhaus had still exponential time worst--case complexity, on average it behaved
as polynomial time algorithm, allowing to compute with large polynomials with integer coefficients.
This breakthrough stimulated the society and, in the following twenty years after Zassenhaus algorithm
was invented, many other algorithms were invented, covering wider range of coefficient domains and
introducing modular techniques (Hensel's lemma) to the case of multivariate polynomials.

Finite fields
-------------

|sympy| supports factoring of polynomials over finite fields only in the univariate case (mostly because
originally factoring over finite fields was needed only as a sub--algorithm of polynomial factorization
routines over integers. In future, we may extend support to multivariate case as well, implementing (for
example) algorithm of [Gathen1983polytime]_. Over finite fields we have a wide variety of algorithms
implemented. There is Berlekamp's algorithm, which uses linear algebra techniques and is suitable for
factoring over small finite fields. We have also Cantor--Zassenhaus' algorithm, which uses polynomial
algebra and is the default factorization algorithm over this domain, because it performs best for average
inputs. There is also algorithm due to Shoup, Gathen and Kaltofen, which is a sub--quadratic time algorithm,
very efficient for large inputs [Gathen1992frobenious]_, [Shoup1993reality]_, [Kaltofen1995subquadratic]_,
[Shoup1995factor]_ (especially for large finite fields, where the binary logarithm of the size of a
finite field is comparable to the degree of an input polynomial). User can switch between different
algorithms at runtime by setting appropriate options in module's configuration.

Integers and rationals
----------------------

Factoring algorithms of univariate and multivariate polynomials over integers and rationals are
currently the most important tools among all factorization routines that were implemented in |sympy|.

Factorization of polynomials over rationals is done by clearing denominators of coefficients of an input
polynomial and performing factorization over integers. As opposed other algorithms, here the results are
not populated back with the common denominator, but integer coefficients are left in the output, and a
rational common multiplicative coefficient of all factors is left in front of others.

In the univariate case |sympy| implements the algorithm of Zassenhaus, which is an exponential time
algorithm, which works by transforming factorization problem over integers to factorization problem
over a small finite field (optimally half--word coefficients, if possible). The resulting factors
are later *lifted* using Hensel's lemma and combined using combinatorial search algorithm to form
*true* univariate factors over integers (also known as searching phase). The last part of this
algorithm makes it exponential time. However, as we previously said, the algorithm behaves as it
had polynomial time complexity, and its true nature is visible only for specially constructed classes
of polynomials (especially those which have very many factors over most or all finite fields). The
unfortunate thing is that polynomials resulting from multivariate or algebraic factoring algorithms
have often exactly those properties. Many heuristics exist to improve the searching phase of Zassenhaus'
algorithm and reduce overall execution time of this method [Abbott2000searching]_.

In 1982, a polynomial time algorithm for univariate factoring over integers of Lenstra, Lenstra and
Lovász was invented [Lenstra1982factor]_. This was the first polynomial time algorithm for the task.
However, it happens that exponential time algorithms are anyway superior for most inputs and the new
algorithm is only beneficial for very large and very badly conditioned inputs. Thus we did not consider
implementing this algorithm in SymPy. There is, however, an algorithm of van Hoeij [vanHoeij2002knapsack]_,
which uses a sub--algorithm of LLL, exactly speaking it uses latice basis reduction, to optimize the
searching phase of Zassenhaus algorithm. van Hoeij's algorithm is actually a family of algorithms and
proper parametrisation is significant to make the algorithm very efficient. A parametrisation and some
additional optimisations, which greatly improve van Hoeij's algorithm, can be found in [Belabas2004relative]_.
The algorithm has still exponential time complexity, but is superior to any other known algorithm for the
taks of univariate polynomials factorization over integers. We plan to implement this algorithm in near
future in |sympy|.

In the multivariate case we implement EEZ algorithm of Wang [Wang1978improved]_, which is an improved
version of Musser's algorithm for multivariate polynomial factorization over integers [Musser1975factor]_,
[Wang1975integers]_. The algorithm works by finding a set of valid substitution integers for all but
one variables. This way a univariate polynomial is constructed which is factored and the resulting
factors are used to compute *true* multivariate factors of the input polynomial. Multivariate factors
are constructed using very efficient parallel (variable--by--variable) Hensel lifting algorithm. The
algorithm tries to predict some of the coefficients during each lifting step, reducing significantly
this way execution times. There are other algorithms that could be implemented in |sympy|, for example
algorithm of Gao [Gao2003partial]_, which factors polynomials via partial differential equations.
However, at this point we do not see a need for implementing another algorithms, because there is
still a lot room for improvements in our implementation of Wang's algorithm.

Algebraic number fields
-----------------------

Currently we use the classical algorithm of Trager [Trager1976algebraic]_ for computing factorizations
of univariate and multivariate polynomials over algebraic number fields. The algorithm was invented as
a side effect of Trager's work on the task of symbolic integration of rational functions. Trager's
algorithm works by transforming algebraic polynomial factorization problem into integer polynomial
factorization problem, which can lead to very large, ill suited polynomials that are hard to factor
(further optimizations are possible, see [Encarnacion1997norms]_). Trager's algorithm support multiple
algebraic extensions by computing a primitive element of all extensions involved. There are other
algorithms, e.g. due to Wang [Wang1976algebraic]_ or Zhi [Zhi1997optimal]_, which can factor with
multiple extensions without computing primitive elements. Benchmarks are, however, not convincing
and it is not clear if those algorithms are really an improvement, comparing to Trager's algorithm
(which is on the other hand much simpler in implementation).

|groebner| bases
================

The method of |groebner| bases is a powerful technique for solving problems in commutative
algebra (polynomial ideal theory, algebraic geometry). In chapter :ref:`thesis-groebner`
we will describe |groebner| bases in very detail, so we will skip any further discussion
on this topic in this section, to avoid redundancy.

Root isolation
==============

Polynomials are solvable by radicals only up to degree 4 (inclusive). This is an unfortunate
but well known consequence of Abel--Ruffini theorem. |sympy| implements heuristic algorithms
for solving polynomials in terms of radicals in :func:`roots` function. In some cases it is
possible to find roots of higher degree polynomials, by taking advantage of polynomial
factorization and decomposition algorithms, and pattern matching.

This is an obviously limited approach and there is a need, in various areas of symbolic
mathematics, e.g. when solving of systems of polynomial equations [Strzebonski1997computing]_,
to compute values of roots of a polynomial to a desired precision. This could be done by using
numerical root finding algorithms, like Durand--Kerner's, which has its implementation in mpmath
library and is exposed to the top--level via :func:`nroots` function. However, in pathological
cases, numerical algorithms may fail to compute correct values of polynomials' roots.

To tackle this problem, when the user needs guaranteed error bounds of the computed roots,
symbolic root isolation algorithms should be used. |sympy| can isolate roots of polynomials with
rational coefficients over real and complex domains, taking advantage of most recent algorithmic
developments in the field. Symbolic root isolation is not that efficient as numerical root finding,
but it is always successful for arbitrary polynomials, giving, as the result, isolation intervals
of the roots of a polynomial, in the real case, or isolation rectangles, in the complex case.

Real roots
----------

For real root isolation |sympy| implements an optimized version [Akritas2008study]_,
[Akritas2008improving]_ of continued fractions algorithm [Collins1976descarte]_. This
approach allows convergence rate to a solution equivalent to convergence rate of continued
fraction expansion of a real number, giving exact results (points instead of intervals)
whenever possible. For a detailed study of computational complexity of continued fractions
algorithm refer to [Sharma2007complexity]_.

Complex roots
-------------

Isolation of complex roots is a much more demanding task. In |sympy| we implemented the algorithm
of Collins and Krandick [Collins1992infallible]_, the best currently known algorithm for symbolic
complex root isolation (it is also implemented in Mathematica, see [MathematicaInternal]_ for
details).

Collins--Krandick algorithm is an infallible (purely symbolic) algorithm for isolating complex
roots of univariate polynomials with rational and Gaussian rational coefficients. In |sympy| we
currently allow only rational coefficients, but extension to the more general domain should be
rather straightforward (Gaussian rational domain has to be implemented).

The algorithm starts with a sufficiently large rectangle, which contains all roots the input
polynomial, it bisects this rectangle, either vertically or horizontally, depending on the
geometry of the isolation rectangle and computes the number of roots in each bisected part.
If there are no roots in a rectangle then such a rectangle is skipped. If there is exactly
one root, then the algorithm returns the rectangle a solution. Otherwise, the new rectangle
is added to a queue and scheduled for further bisection. The initial rectangle is computed
using Cauchy bound, which may give large overestimation on the magnitude of roots. If the
there are no more rectangles left, i.e. each resulting rectangle contains only a single
root (is an isolation rectangle), then the algorithm terminates. After the isolation phase,
resulting rectangles can be further refined to the desired precision.

As only rational coefficients are allowed, this gives the possibility of improving the speed
of computations by isolating strictly complex roots only in the upper half--plane, excluding
the real line (positive imaginary component). Conjugates are located by symmetry and real
roots are located using much more efficient real root isolation algorithm.

An important issue is location of roots on the boundary of an isolation rectangle. The
algorithm can easily count roots in such setup (as opposed to other complex root isolation
algorithm). However, to disambiguate the bisection scheme, where the same could be counted
as a part of two (or more) adjacent rectangles, we only count roots located on the northern
and western edges, and on the north--western corner of an isolation rectangle.

The current implementation of Collins--Krandick algorithm in |sympy| is suboptimal and there
are several possible enhancements, some of listed in [Collins1992infallible]_, which ought
to make complex root isolation in |sympy| much faster.

Collins--Krandick algorithm seems to be a good candidate for parallelization on multiple
processors, although the author is not aware of any work tackling this problem. An approach
would be to schedule refinement of particular isolation rectangles or clusters of rectangles
on different processors. Currently we simply maintain a queue of rectangles in order from
the smallest to the largest and refine each one--by--one on a single CPU.

Previously also we experimented with, so called, global bisection algorithm due to Wilf
[Wilf1978bisection]_. As its name suggests, Wilf's algorithm takes advantage of bisection
scheme and operates on rectangles, similarly to Collins--Krandick algorithm, however it uses
Sturm sequences to compute the number of roots in a rectangle and thus is very slow, because
computing polynomial remainder sequences (in particular Sturm sequences) is slow a computationally
demanding process. The other issue is that when a root is located on or even near (there is no
definition of the word *near* in this context) rectangle boundary then the algorithm has to be
restarted with an updated initial configuration. This makes global bisection algorithm fragile
and unpredictable. There are other approaches to symbolic root isolation, see for example
[Pinkert1976complex]_.

Collins--Krandick algorithm takes advantage of purely symbolic approach, thus is significantly
slower than rapidly converging numerical algorithms. However, it is possible to turn it into a
mixed symbolic--numerical algorithm, where, in certain conditions, it is possible to replace
symbolic computations with validated numerical computations, without compromising properties
of the original algorithm.

It should be obvious that real root isolation is less computationally intensive than complex
root isolation, so whenever it is known that only real (or even negative or positive) roots
are required, then the domain of computation should be appropriately limited to speed up the
computations (for a detailed discussion see [Collins1996complex]_).

Conclusions
===========

In this chapter we gave a brief description to the most important algorithms of polynomials
manipulation module. There are other algorithms that were implemented in the module, which
also deserve attention and a few words of explanation. Hopefully in some foreseeable future
we will be able to write a more capacious volume, in which we will describe all of them. We
also gave references to the most influential literature that was used to implement those
algorithms or seems promising for further developments in near future. We consider this a
good starting point for people who would be interested in picking up some development tasks
to improve the module.

