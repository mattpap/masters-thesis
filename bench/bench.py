
"""
f = Poly(27*x + y**2 - 15*z)
%time f**10;
# Wall time: 0.02 s
# Wall time: 0.01 s
%time f**20;
# Wall time: 0.26 s
# Wall time: 0.18 s
%time f**30;
# Wall time: 2.25 s
# Wall time: 1.53 s
%time f**40;
# Wall time: 4.93 s
# Wall time: 3.33 s
%time f**50;
# Wall time: 21.67 s
# Wall time: 14.92 s
"""

from matplotlib import pyplot as plt
X = [10, 20, 30, 40, 50]
Y_python = [0.02, 0.26, 2.25, 4.93, 21.67]
Y_cython = [0.01, 0.18, 1.53, 3.33, 14.92]
plt.plot(X, Y_python, 'bo-', X, Y_cython, 'ro-')
plt.legend(('Python', 'Cython'), loc='upper left')
plt.xlabel('Exponent ($n$)')
plt.ylabel('Time [s]')
plt.title('$(27 x + y^2 - 15 z)^n$')
plt.grid()
plt.savefig('cython-power.pdf')
plt.show()

"""
%time u = factor(x**200-1)
# Wall time: 0.28 s
# Wall time: 0.19 s
%time u = factor(x**400-1)
# Wall time: 0.85 s
# Wall time: 0.67 s
%time u = factor(x**600-1)
# Wall time: 3.18 s
# Wall time: 2.37 s
%time u = factor(x**800-1)
# Wall time: 3.76 s
# Wall time: 2.87 s
%time u = factor(x**1000-1)
# Wall time: 5.06 s
# Wall time: 3.82 s
%time u = factor(x**1200-1)
# Wall time: 11.64 s
# Wall time: 8.76 s
%time u = factor(x**1400-1)
# Wall time: 15.13 s
# Wall time: 11.50 s
"""

from matplotlib import pyplot as plt
X = [200, 400, 600, 800, 1000, 1200, 1400]
Y_python = [0.28, 0.85, 3.18, 3.76, 5.06, 11.64, 15.13]
Y_cython = [0.19, 0.67, 2.37, 2.87, 3.82, 8.76, 11.50]
plt.plot(X, Y_python, 'bo-', X, Y_cython, 'ro-')
plt.legend(('Python', 'Cython'), loc='upper left')
plt.xlabel('Exponent ($n$)')
plt.ylabel('Time [s]')
plt.title('$factor\\left(x^n - 1\\right)$')
plt.grid()
plt.savefig('cython-factor.pdf')
plt.show()

"""
%time dmp_pow(F2, 5, 2, ZZ);
Wall time: 0.02 s
%time dmp_pow(F2, 10, 2, ZZ);
Wall time: 0.24 s
%time dmp_pow(F2, 15, 2, ZZ);
Wall time: 2.10 s
%time dmp_pow(F2, 20, 2, ZZ);
Wall time: 4.81 s
%time dmp_pow(F2, 25, 2, ZZ);
Wall time: 22.16 s

%time sdp_pow(G2, 5, 2, lex, ZZ);
Wall time: 0.02 s
%time sdp_pow(G2, 10, 2, lex, ZZ);
Wall time: 0.61 s
%time sdp_pow(G2, 15, 2, lex, ZZ);
Wall time: 6.23 s
%time sdp_pow(G2, 20, 2, lex, ZZ);
Wall time: 18.80 s
%time sdp_pow(G2, 25, 2, lex, ZZ);
Wall time: 89.93 s


%time dmp_pow(F3, 5, 2, ZZ);
Wall time: 0.01 s
%time dmp_pow(F3, 10, 2, ZZ);
Wall time: 0.09 s
%time dmp_pow(F3, 15, 2, ZZ);
Wall time: 0.97 s
%time dmp_pow(F3, 20, 2, ZZ);
Wall time: 2.02 s
%time dmp_pow(F3, 25, 2, ZZ);
Wall time: 9.16 s
%time dmp_pow(F3, 30, 2, ZZ);
Wall time: 26.71 s

%time sdp_pow(G3, 5, 2, lex, ZZ);
Wall time: 0.00 s
%time sdp_pow(G3, 10, 2, lex, ZZ);
Wall time: 0.06 s
%time sdp_pow(G3, 15, 2, lex, ZZ);
Wall time: 0.54 s
%time sdp_pow(G3, 20, 2, lex, ZZ);
Wall time: 1.55 s
%time sdp_pow(G3, 25, 2, lex, ZZ);
Wall time: 6.69 s
%time sdp_pow(G3, 30, 2, lex, ZZ);
Wall time: 19.99 s


%time dmp_pow(F1, 5, 2, ZZ);
Wall time: 0.00 s
%time dmp_pow(F1, 10, 2, ZZ);
Wall time: 0.01 s
%time dmp_pow(F1, 15, 2, ZZ);
Wall time: 0.10 s
%time dmp_pow(F1, 20, 2, ZZ);
Wall time: 0.23 s
%time dmp_pow(F1, 25, 2, ZZ);
Wall time: 0.75 s
%time dmp_pow(F1, 30, 2, ZZ);
Wall time: 1.94 s

%time sdp_pow(G1, 5, 2, lex, ZZ);
Wall time: 0.00 s
%time sdp_pow(G1, 10, 2, lex, ZZ);
Wall time: 0.00 s
%time sdp_pow(G1, 15, 2, lex, ZZ);
Wall time: 0.01 s
%time sdp_pow(G1, 20, 2, lex, ZZ);
Wall time: 0.03 s
%time sdp_pow(G1, 25, 2, lex, ZZ);
Wall time: 0.10 s
%time sdp_pow(G1, 30, 2, lex, ZZ);
Wall time: 0.19 s

"""

"""
from sympy.polys.densebasic import dmp_to_dict
from sympy.polys.densearith import dmp_pow

from sympy.polys.monomialtools import monomial_key, monomials
from sympy.polys.groebnertools import sdp_from_dict, sdp_pow

lex = monomial_key('lex')

f1 = Poly(x + y + z)
F1 = f1.rep.rep
G1 = sdp_from_dict(dmp_to_dict(F1, 2), lex)

f2 = Poly(sum(list(monomials((x, y, z), 2))))
F2 = f2.rep.rep
G2 = sdp_from_dict(dmp_to_dict(F2, 2), lex)

f3 = Poly(sum(list(monomials((x, y, z), 2))[::2]))
F3 = f3.rep.rep
G3 = sdp_from_dict(dmp_to_dict(F3, 2), lex)
"""

from matplotlib import pyplot as plt
X1 = [5, 10, 15, 20, 25]
Y1_dense = [0.02, 0.24, 2.10, 4.81, 22.16]
Y1_sparse = [0.02, 0.61, 6.23, 18.80, 89.93]
plt.plot(X1, Y1_dense, 'bo-', X1, Y1_sparse, 'ro-')
plt.legend(('dense', 'sparse'), loc='upper left')
plt.xlabel('Exponent ($n$)')
plt.ylabel('Time [s]')
plt.title('100% dense polynomial exponentiation')
plt.grid()
plt.savefig('100-dense-power.pdf')
plt.show()

from matplotlib import pyplot as plt
X2 = [5, 10, 15, 20, 25, 30]
Y2_dense = [0.01, 0.09, 0.97, 2.02, 9.16, 26.71]
Y2_sparse = [0.00, 0.06, 0.54, 1.55, 6.69, 19.99]
plt.plot(X2, Y2_dense, 'bo-', X2, Y2_sparse, 'ro-')
plt.legend(('dense', 'sparse'), loc='upper left')
plt.xlabel('Exponent ($n$)')
plt.ylabel('Time [s]')
plt.title('50% dense polynomial exponentiation')
plt.grid()
plt.savefig('50-dense-power.pdf')
plt.show()

from matplotlib import pyplot as plt
X3 = [5, 10, 15, 20, 25, 30]
Y3_dense = [0.00, 0.01, 0.10, 0.23, 0.75, 1.94]
Y3_sparse = [0.00, 0.00, 0.01, 0.03, 0.10, 0.19]
plt.plot(X3, Y3_dense, 'bo-', X3, Y3_sparse, 'ro-')
plt.legend(('dense', 'sparse'), loc='upper left')
plt.xlabel('Exponent ($n$)')
plt.ylabel('Time [s]')
plt.title('sparse polynomial exponentiation: $(x + y + z)^n$')
plt.grid()
plt.savefig('sparse-power.pdf')
plt.show()

from matplotlib import pyplot as plt
X = [100, 200, 300, 400, 500, 600, 700, 800]
Y_sympy = [0.33, 1.19, 4.15, 4.23, 5.79, 15.88, 17.07, 19.24]
Y_python = [0.06, 0.19, 0.59, 0.58, 0.75, 2.07, 2.09, 2.38]
Y_gmpy = [0.08, 0.26, 0.88, 0.87, 1.16, 3.14, 3.33, 3.81]
plt.plot(X, Y_sympy, 'bo-', X, Y_python, 'ro-', X, Y_gmpy, 'go-')
plt.legend(('sympy', 'python', 'gmpy'), loc='upper left')
plt.xlabel('Exponent ($n$)')
plt.ylabel('Time [s]')
plt.title('$factor(x^n - 1)$')
plt.grid()
plt.savefig('ground-factor-small.pdf')
plt.show()

"""
for i in xrange(0, 9):
    f = expand((1234*x + 123*y + 12*z + 1)**(10+i))
    F = Poly(f, domain=ZZ_sympy())
    G = Poly(f, domain=ZZ_python())
    H = Poly(f, domain=ZZ_gmpy())
    %time F.factor_list()
    %time G.factor_list()
    %time H.factor_list()

CPU times: user 0.50 s, sys: 0.00 s, total: 0.50 s
Wall time: 0.61 s
Out[95]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 10)])
CPU times: user 0.26 s, sys: 0.00 s, total: 0.26 s
Wall time: 0.32 s
Out[96]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 10)])
CPU times: user 0.12 s, sys: 0.00 s, total: 0.12 s
Wall time: 0.17 s
Out[97]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 10)])
CPU times: user 0.82 s, sys: 0.00 s, total: 0.82 s
Wall time: 0.99 s
Out[98]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 11)])
CPU times: user 0.44 s, sys: 0.00 s, total: 0.44 s
Wall time: 0.53 s
Out[99]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 11)])
CPU times: user 0.18 s, sys: 0.00 s, total: 0.18 s
Wall time: 0.23 s
Out[100]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 11)])
CPU times: user 1.23 s, sys: 0.00 s, total: 1.24 s
Wall time: 1.47 s
Out[101]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 12)])
CPU times: user 0.74 s, sys: 0.00 s, total: 0.74 s
Wall time: 0.92 s
Out[102]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 12)])
CPU times: user 0.24 s, sys: 0.00 s, total: 0.24 s
Wall time: 0.30 s
Out[103]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 12)])
CPU times: user 1.93 s, sys: 0.00 s, total: 1.93 s
Wall time: 2.26 s
Out[104]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 13)])
CPU times: user 1.28 s, sys: 0.00 s, total: 1.28 s
Wall time: 1.52 s
Out[105]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 13)])
CPU times: user 0.34 s, sys: 0.00 s, total: 0.34 s
Wall time: 0.49 s
Out[106]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 13)])
CPU times: user 2.96 s, sys: 0.01 s, total: 2.97 s
Wall time: 3.52 s
Out[107]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 14)])
CPU times: user 2.12 s, sys: 0.00 s, total: 2.12 s
Wall time: 2.56 s
Out[108]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 14)])
CPU times: user 0.46 s, sys: 0.00 s, total: 0.46 s
Wall time: 0.57 s
Out[109]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 14)])
CPU times: user 4.49 s, sys: 0.01 s, total: 4.50 s
Wall time: 5.34 s
Out[110]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 15)])
CPU times: user 3.45 s, sys: 0.01 s, total: 3.46 s
Wall time: 4.16 s
Out[111]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 15)])
CPU times: user 0.63 s, sys: 0.00 s, total: 0.63 s
Wall time: 0.75 s
Out[112]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 15)])
CPU times: user 6.80 s, sys: 0.01 s, total: 6.81 s
Wall time: 8.10 s
Out[113]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 16)])
CPU times: user 5.55 s, sys: 0.01 s, total: 5.56 s
Wall time: 6.59 s
Out[114]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 16)])
CPU times: user 0.85 s, sys: 0.00 s, total: 0.85 s
Wall time: 1.01 s
Out[115]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 16)])
CPU times: user 10.30 s, sys: 0.04 s, total: 10.33 s
Wall time: 12.38 s
Out[116]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 17)])
CPU times: user 8.78 s, sys: 0.02 s, total: 8.80 s
Wall time: 10.43 s
Out[117]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 17)])
CPU times: user 1.13 s, sys: 0.00 s, total: 1.14 s
Wall time: 1.37 s
Out[118]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 17)])
CPU times: user 15.44 s, sys: 0.02 s, total: 15.46 s
Wall time: 18.37 s
Out[119]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 18)])
CPU times: user 13.61 s, sys: 0.02 s, total: 13.62 s
Wall time: 15.99 s
Out[120]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 18)])
CPU times: user 1.51 s, sys: 0.00 s, total: 1.51 s
Wall time: 1.77 s
Out[121]: (1, [(Poly(1234*x + 123*y + 12*z + 1, x, y, z, domain='ZZ'), 18)])
"""

from matplotlib import pyplot as plt
X = [10, 11, 12, 13, 14, 15, 16, 17, 18]
Y_sympy = [0.61, 0.99, 1.47, 2.26, 3.52, 5.34, 8.10, 12.38, 18.37]
Y_python = [0.32, 0.53, 0.92, 1.52, 2.56, 4.16, 6.59, 10.43, 15.99]
Y_gmpy = [0.17, 0.23, 0.30, 0.49, 0.57, 0.75, 1.01, 1.37, 1.77]
plt.plot(X, Y_sympy, 'bo-', X, Y_python, 'ro-', X, Y_gmpy, 'go-')
plt.legend(('sympy', 'python', 'gmpy'), loc='upper left')
plt.xlabel('Exponent ($n$)')
plt.ylabel('Time [s]')
plt.title('$factor((1234 x + 123 y + 12 z + 1)^n)$')
plt.grid()
plt.savefig('ground-factor-large.pdf')
plt.show()

