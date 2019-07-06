import copy
import fractions
import operator

from typing import List, Union


class _LLLVector(list):
    def __init__(self, x):
        super(_LLLVector, self).__init__(map(fractions.Fraction, x))

    def self_dot_product(self) -> fractions.Fraction:
        return self.dot_product(self)

    square = self_dot_product

    def dot_product(self, other: "_LLLVector") -> fractions.Fraction:
        if len(self) != len(other):
            raise ValueError("dot_product(): length not equal")

        return sum(map(operator.mul, self, other))

    def projection(self, other: "_LLLVector") -> fractions.Fraction:
        if len(self) != len(other):
            raise ValueError("projection(): length not equal")

        return self.dot_product(other) / self.self_dot_product()

    def projection_vector(self, other: "_LLLVector") -> "_LLLVector":
        if len(self) != len(other):
            raise ValueError("projection_vector(): length not equal")

        return self.projection(other) * self

    def __add__(self, other: "_LLLVector") -> "_LLLVector":
        if len(self) != len(other):
            raise ValueError("__add__(): length not equal")

        return _LLLVector(map(operator.add, self, other))

    def __sub__(self, other: "_LLLVector") -> "_LLLVector":
        if len(self) != len(other):
            raise ValueError("__sub__(): length not equal")

        return _LLLVector(map(operator.sub, self, other))

    def __mul__(self, other: Union[int, fractions.Fraction]):
        if isinstance(other, int):
            other = fractions.Fraction(other)

        if not isinstance(other, fractions.Fraction):
            return NotImplemented

        return _LLLVector(map(lambda x: x * other, self))

    def __rmul__(self, other: Union[int, fractions.Fraction]):
        if isinstance(other, int):
            other = fractions.Fraction(other)

        if not isinstance(other, fractions.Fraction):
            return NotImplemented

        return _LLLVector(map(lambda x: x * other, self))

    def __repr__(self) -> str:
        return '_LLLVector([{}])'.format(', '.join(map(str, self)))


class _LLLMatrix(list):
    pass


def _gram_schmidt(v: List[_LLLVector]) -> List[_LLLVector]:
    u = []

    for v_i in v:
        u_i = copy.deepcopy(v_i)

        for u_j in u:
            u_i = u_i - u_j.projection_vector(v_i)

        if any(u_i):
            u.append(u_i)

    return u


def lll(m: List[List[int]], delta: float) -> List[List[int]]:
    n = len(m)
    m = list(map(_LLLVector, m))
    orthodox_basis = _gram_schmidt(m)

    def _mu(i_: int, j_: int) -> fractions.Fraction:
        return orthodox_basis[j_].projection(_LLLVector(m[i_]))

    k = 1
    while k < n:
        for j in range(k - 1, -1, -1):
            mu_k_j = _mu(k, j)

            if abs(mu_k_j) > (1 / 2):
                m[k] = m[k] - m[j] * round(mu_k_j)
                orthodox_basis = _gram_schmidt(m)

        if orthodox_basis[k].square() >= (delta - _mu(k, k - 1) ** 2) * orthodox_basis[k - 1].square():
            k += 1
        else:
            m[k], m[k - 1] = m[k - 1], m[k]
            orthodox_basis = _gram_schmidt(m)
            k = max(k - 1, 1)

    return [list(map(int, b)) for b in m]


