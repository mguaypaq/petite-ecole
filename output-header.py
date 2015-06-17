r"""
Sage script which contains precomputed data on q-chromatic symmetric functions.
"""

from sage.combinat.sf.sfa import zee
R, q = QQ['q'].objgen()
sym = SymmetricFunctions(R)
e = sym.e()
h = sym.h()
m = sym.m()
p = sym.p()
s = sym.s()

# q-chromatic symmetric functions for unit interval orders.
# There is one of each for each Dyck path.

#--------------------------------
# conjecture
#--------------------------------

# The q-csf is e-positive
# (so that it should actually be a graded permutation representation).

def is_e_positive(symfunc):
    return all(
        coefficient >= 0
        for partition, polynomial in e(symfunc)
        for coefficient in polynomial
        )

def test_conjecture():
    r"""
    Test whether q-csf is e-positive.
    """
    return all(
        is_e_positive(csf[path])
        for path in csf
        )

#--------------------------------
# data
#--------------------------------

csf = {}

