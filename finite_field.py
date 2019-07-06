# 以下的操作都是采用多项式表示
# 为了效率，各方法的参数都是整数，但其实应该给各有限域的元新建一个类
import numbers
from typing import List

import primality_test
import gcd


class _PrimeFiniteFieldElementParent(numbers.Integral):
    def __trunc__(self):
        return NotImplemented

    def __floor__(self):
        return NotImplemented

    def __ceil__(self):
        return NotImplemented

    def __round__(self, ndigits=None):
        return NotImplemented

    def __rfloordiv__(self, other):
        return NotImplemented

    def __rmod__(self, other):
        return NotImplemented

    def __lt__(self, other):
        return NotImplemented

    def __le__(self, other):
        return NotImplemented

    def __radd__(self, other):
        return NotImplemented

    def __pos__(self):
        return NotImplemented

    def __rmul__(self, other):
        return NotImplemented

    def __rtruediv__(self, other):
        return NotImplemented

    def __rpow__(self, base):
        return NotImplemented

    def __abs__(self):
        return NotImplemented

    def __pow__(self, exponent, modulus=None):
        return NotImplemented

    def __lshift__(self, other):
        return NotImplemented

    def __rlshift__(self, other):
        return NotImplemented

    def __rshift__(self, other):
        return NotImplemented

    def __rrshift__(self, other):
        return NotImplemented

    def __and__(self, other):
        return NotImplemented

    def __rand__(self, other):
        return NotImplemented

    def __xor__(self, other):
        return NotImplemented

    def __rxor__(self, other):
        return NotImplemented

    def __or__(self, other):
        return NotImplemented

    def __ror__(self, other):
        return NotImplemented

    def __invert__(self):
        return NotImplemented

    # not intended for direct usage
    p = None

    def __init__(self, *args):
        if len(args) > 2:
            raise TypeError("__init__() takes at most 1 positional argument, %d given" % len(args))

        if len(args) == 0:
            self.data = 0

        if len(args) == 1:
            self.data = args[0] % self.p

    def __str__(self):
        _header = type(self).__qualname__ + '('
        _template = 'p=%d, data=%d'
        _footer = ')'

        return _header + _template % (self.p, self.data) + _footer

    def __int__(self):
        return self.data

    def __add__(self, other):
        if isinstance(other, int):
            other = self.__class__(other)

        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.p != other.p:
            raise ValueError("self.p != other.p")

        return type(self)((self.data + other.data) % self.p)

    def __sub__(self, other):
        if isinstance(other, int):
            other = self.__class__(other)

        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.p != other.p:
            raise ValueError("self.p != other.p")

        return type(self)((self.data - other.data) % self.p)

    def __mul__(self, other):
        if isinstance(other, int):
            other = self.__class__(other)

        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.p != other.p:
            raise ValueError("self.p != other.p")

        return type(self)((self.data * other.data) % self.p)

    def __rmul__(self, other):
        if isinstance(other, int):
            other = self.__class__(other)

        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.p != other.p:
            raise ValueError("self.p != other.p")

        return type(self)((self.data * other.data) % self.p)

    def __truediv__(self, other):
        if isinstance(other, int):
            other = self.__class__(other)

        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.p != other.p:
            raise ValueError("self.p != other.p")

        try:
            inverse = gcd.get_modular_inverse(other.data, other.p)
            return type(self)((self.data * inverse) % self.p)
        except ValueError:
            raise

    def __floordiv__(self, other):
        return NotImplemented

    def __mod__(self, other):
        raise ValueError("wtf")

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.p == other.p and self.data == other.data

    def __neg__(self):
        return type(self)(-self.data % self.p)


def get_prime_finite_field_element_class(p: int, name: str) -> type:
    _primality_test_iterations = 10

    if not primality_test.primality_test(p, _primality_test_iterations):
        raise ValueError("p is not prime")

    result = type(name, (_PrimeFiniteFieldElementParent,), {'p': p})
    return result


class _PrimeFiniteFieldPowerParent(object):
    p = None
    n = None
    mod_poly = None

    def __init__(self, *args):
        if len(args) == 1:
            data = args[0]
            self.data = list(list(reversed(data))[i] for i in range(self.n))
            return

        if len(args) == 0:
            self.data = list(0 for _ in range(self.n + 1))
            return

        raise ValueError("__init__(): too many arguments")

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        result = self.__class__()

        result.data = list(x + y for x, y in zip(self.data, other.data))

        return result

    def __sub__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        result = self.__class__()

        result.data = list(x - y for x, y in zip(self.data, other.data))

        return result

    def __neg__(self):
        result = self.__class__()

        result.data = list(-x for x in self.data)

        return result

    def __rmul__(self, other):
        if not isinstance(other, self.__class__) and not isinstance(other, numbers.Integral):
            return NotImplemented

        if isinstance(other, numbers.Integral):
            result = self.__class__()

            result.data = list(other * x for x in self.data)

            return result

        if isinstance(other, self.__class__):
            # call __mul__()
            return self * other

    def __mul__(self, other):
        if not isinstance(other, self.__class__) and not isinstance(other, numbers.Integral):
            return NotImplemented

        if isinstance(other, numbers.Integral):
            result = self.__class__()

            result.data = list(other * x for x in self.data)

            return result

        if isinstance(other, self.__class__):
            result = self.__class__()

            tmp_list = [self.data[0].__class__(0) for _ in range(2 * self.n + 1)]

            for i in range(len(self.data)):
                for j in range(len(other.data)):
                    tmp_list[i + j] = self.data[i] * other.data[j]

            tmp_highest_non_zero_index = len(tmp_list) - 1

            while tmp_highest_non_zero_index > self.n:
                tmp_highest_non_zero_index = 0

                for i in reversed(range(len(tmp_list))):
                    if tmp_list[i] != tmp_list[0].__class__(0):
                        tmp_highest_non_zero_index = i
                        break

                inv = self.data[0].__class__(1) / self.mod_poly[-1]

                annihilator_list = [inv * x * tmp_list[tmp_highest_non_zero_index] for x in self.mod_poly]

                print('annihilator: ' + ', '.join(map(str, annihilator_list)))

                tmp_list[tmp_highest_non_zero_index:tmp_highest_non_zero_index - self.n - 2:-1] = \
                    list(x - y for x, y in zip(tmp_list[tmp_highest_non_zero_index:tmp_highest_non_zero_index - self.n - 2:-1],
                                               annihilator_list))

                for i in range(tmp_highest_non_zero_index,
                               tmp_highest_non_zero_index - self.n - 2,
                               -1):
                    tmp_list[i] -= annihilator_list[i - tmp_highest_non_zero_index + len(annihilator_list) - 1]

                print(', '.join(map(str, tmp_list)))

            tmp_list = tmp_list[:self.n]

            result.data = tmp_list

            return result

    def __str__(self):
        result = ''
        result += type(self).__qualname__
        result += '('

        result += 'n=%s, ' % str(self.n)
        result += '\n'
        result += 'mod_poly=%s, ' % ' + '.join(map(
            lambda x: str(x[1]) + '*x^' + str(len(self.mod_poly) - x[0] - 1),
            enumerate(reversed(self.mod_poly))))
        result += '\n'
        result += 'poly=%s' % ' + '.join(map(
            lambda x: str(x[1]) + '*x^' + str(len(self.data) - x[0] - 1),
            enumerate(reversed(self.data))
        ))

        result += ')'

        return result


def get_prime_finite_field_power_element_class(n: int, mod_poly: List[int], name: str) -> type:
    if len(mod_poly) != n + 1 or mod_poly[-1] == 0:
        raise ValueError("get_prime_finite_field:power_element_class(): invalid mod poly")

    result = type(name, (_PrimeFiniteFieldPowerParent,),
                  {'n': n, 'mod_poly': list(reversed(mod_poly))})

    return result


class SM9G2(object):
    def __init__(self, *args):
        if len(args) == 2:
            self.is_int = False
            a_1, a_2 = args

            self.a_1 = a_1
            self.a_2 = a_2
            return

        if len(args) == 1:
            self.is_int = True
            self.data = args[0]
            return

        raise ValueError("__init__(): invalid arguments")

    def __add__(self, other):
        if not isinstance(other, SM9G2):
            return NotImplemented

        if self.is_int ^ other.is_int == 1:
            return NotImplemented

        if self.is_int:
            return SM9G2(self.data + other.data)
        else:
            return SM9G2(self.a_1 + other.a_1, self.a_2 + other.a_2)

    def __sub__(self, other):
        if not isinstance(other, SM9G2):
            return NotImplemented

        if self.is_int ^ other.is_int == 1:
            return NotImplemented

        if self.is_int:
            return SM9G2(self.data + other.data)
        else:
            return SM9G2(self.a_1 - other.a_1, self.a_2 - other.a_2)

    def __mul__(self, other):
        if not isinstance(other, SM9G2):
            return NotImplemented

        if not self.is_int:
            if not other.is_int:
                return SM9G2(self.a_1 * other.a_2 + self.a_2 * other.a_1,
                             self.a_2 * other.a_2 - self.a_1.__class__(2) * self.a_1 * other.a_1)
            else:
                if other.data == 1:
                    return self

                if other.data == 2:
                    return self + self

                result = SM9G2(0, 0)
                curr_item = None

                for bit in reversed(bin(self.data)[2:]):
                    if curr_item is None:
                        curr_item = SM9G2(self.a_1, self.a_2)
                    else:
                        curr_item = curr_item + curr_item

                    if bit == '1':
                        result += curr_item

                return result
        else:
            if other.is_int:
                return SM9G2(self.data * other.data)
            else:
                if self.data == 1:
                    return other

                if self.data == 2:
                    return other + other

                result = SM9G2(0, 0)
                curr_item = None

                for bit in reversed(bin(self.data)[2:]):
                    if curr_item is None:
                        curr_item = SM9G2(other.a_1, other.a_2)
                    else:
                        curr_item = curr_item + curr_item

                    if bit == '1':
                        result += curr_item

            return result

    def __rmul__(self, other):
        if not isinstance(other, SM9G2):
            return NotImplemented

        if not self.is_int:
            if not other.is_int:
                return SM9G2(self.a_1 * other.a_2 + self.a_2 * other.a_1,
                             self.a_2 * other.a_2 - self.a_1.__class__(2) * self.a_1 * other.a_1)
            else:
                if other.data == 1:
                    return self

                if other.data == 2:
                    return self + self

                result = SM9G2(0, 0)
                curr_item = None

                for bit in reversed(bin(self.data)[2:]):
                    if curr_item is None:
                        curr_item = SM9G2(self.a_1, self.a_2)
                    else:
                        curr_item = curr_item + curr_item

                    if bit == '1':
                        result += curr_item

                return result
        else:
            return NotImplemented

    def __truediv__(self, other):
        other_inv = SM9G2(-other.a_1 / (other.a_2 * other.a_2 + 2 * other.a_1 * other.a_1),
                          other.a_2 / (other.a_2 * other.a_2 + 2 * other.a_1 * other.a_1))

        return self * other_inv

    def get_inv(self):
        self_inv = SM9G2(-self.a_1 / (self.a_2 * self.a_2 + 2 * self.a_1 * self.a_1),
                         self.a_2 / (self.a_2 * self.a_2 + 2 * self.a_1 * self.a_1))

        return self_inv

    def __str__(self):
        result = ''

        if not self.is_int:
            result += 'SM9G2('
            result += 'a_1='
            result += str(self.a_1)
            result += ', '
            result += 'a_2='
            result += str(self.a_2)
            result += ')'
        else:
            result += 'SM9G2('
            result += 'is_int, data='
            result += str(self.data)
            result += ')'

        return result

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        if self.is_int != other.is_int:
            return False

        if self.is_int:
            return self.data == other.data
        else:
            return self.a_1 == other.a_1 and self.a_2 == other.a_2


class GF2Power31(object):
    _element_bit_length = 31
    _element_bitmask = (1 << _element_bit_length) - 1

    def __init__(self: "GF2Power31", data: int) -> None:
        self.data = data

        if data & self._element_bitmask != data:
            raise ValueError("__init__(): data to large")

    def __repr__(self: "GF2Power31") -> str:
        return self.__class__.__qualname__ + '(' + str(self.data) + ')'

    def __add__(self: "GF2Power31", other: "GF2Power31") -> "GF2Power31":
        if not isinstance(other, self.__class__):
            return NotImplemented

        a = self.data
        b = other.data
        c = a + b
        c = (c & self._element_bitmask) + (c >> 31)

        return GF2Power31(c)

    def __sub__(self: "GF2Power31", other: "GF2Power31") -> "GF2Power31":
        return NotImplemented

    def __mul__(self: "GF2Power31", other: "GF2Power31") -> "GF2Power31":
        if not isinstance(other, self.__class__):
            return NotImplemented

        a = self.data
        b = other.data
        result = (a * b) % self._element_bitmask

        return GF2Power31(result)


# GF(2^4) 的本原多项式为 x^4 + x + 1
GF_2_4_PRIM_POLY = 0x13


def _gf_2_4_check(a: int) -> None:
    # GF(2^4) 中元占 4 位
    if not (0 <= a <= 15):
        raise ValueError("_gf_2_4_check: invalid gf(2^4) element %d" % a)


def gf_2_4_add(a: int, b: int) -> int:
    _gf_2_4_check(a)
    _gf_2_4_check(b)

    return gf_2_4_add_nocheck(a, b)


def gf_2_4_add_nocheck(a: int, b: int) -> int:
    return a ^ b


gf_2_4_sub = gf_2_4_add
gf_2_4_sub_nocheck = gf_2_4_add_nocheck


def gf_2_4_check_prim_poly(prim_poly: int):
    pass


def gf_2_4_mul_x(a: int, prim_poly: int = GF_2_4_PRIM_POLY) -> int:
    _gf_2_4_check(a)
    if prim_poly != GF_2_4_PRIM_POLY:
        _gf_2_4_check_prim_poly(prim_poly)

    return gf_2_4_mul_x_nocheck(a, prim_poly=prim_poly)


def gf_2_4_mul_x_nocheck(a: int, prim_poly: int = GF_2_4_PRIM_POLY) -> int:
    # 看对应的多项式 3 次项是否为 1，需要用位掩码 0x8 判断
    if a & 0x8 == 0x8:
        # 如果对应的多项式 3 次项为 1，那么先异或 0x8 减去最高次项，再左移一位，
        # 然后异或 0x3 (x + 1)，这相当于先左移一位再模掉 x^4 + x + 1
        # 其他多项式同理
        return ((a ^ 0x8) << 1) ^ (prim_poly & 0xf)
    else:
        # 否则只需要左移一位即可
        return a << 1


def gf_2_4_mul(a: int, b: int, prim_poly: int = GF_2_4_PRIM_POLY) -> int:
    _gf_2_4_check(a)
    _gf_2_4_check(b)
    if prim_poly != GF_2_4_PRIM_POLY:
        _gf_2_4_check_prim_poly(prim_poly)

    return gf_2_4_mul_nocheck(a, b, prim_poly=prim_poly)


def gf_2_4_mul_nocheck(a: int, b: int, \
                       prim_poly: int = GF_2_4_PRIM_POLY) -> int:
    # GF(2^4) 中的零元是 0x0，这与取哪个多项式做本原多项式无关
    result = 0x0
    a_mul = a

    for i in range(4):
        bitmask = 1 << i

        if b & bitmask == bitmask:
            result = gf_2_4_add_nocheck(result, a_mul)

        a_mul = gf_2_4_mul_x_nocheck(a_mul, prim_poly=prim_poly)

    return result


def gf_2_4_get_inverse(a: int, prim_poly: int = GF_2_4_PRIM_POLY) -> int:
    _gf_2_4_check(a)
    _gf_2_4_check_prim_poly(a)

    if (a == 0x0):
        raise ValueError("gf_2_4_get_inverse: 0x0 has no inverse" % a)

    return gf_2_4_get_inverse_nocheck(a, prim_poly=prim_poly)


_gf_2_4_inverse_lookup_table = \
    [0, 1, 9, 14, 13, 11, 7, 6, 15, 2, 12, 5, 10, 4, 3, 8]


def gf_2_4_get_inverse_nocheck_lookup_table(a: int,
                                            prim_poly: int = GF_2_4_PRIM_POLY) -> int:
    # 实际上 _gf_2_4_inverse_lookup_table[0] 没用
    return _gf_2_4_inverse_lookup_table[a]


def gf_2_4_get_inverse_nocheck_exponential(a: int,
                                           prim_poly: int = GF_2_4_PRIM_POLY) -> int:
    # 对于 GF(2^4) 中任一非零元 g，它的逆元一定是它的 2^4 - 2 = 14 次方
    # 这可以通过指数的性质得以证明

    # GF(2^4) 中的单位元是 0x1，这与取哪个多项式做本原多项式无关
    result = 0x1

    # 重复 3 遍平方和加法运算，即可算出任一元的 14 次方
    # 先令要加的项为 a, 再重复三遍先把单独一项平方，然后乘到结果上的操作
    # 这样也能避免侧信道攻击
    item = a

    for i in range(3):
        item = gf_2_4_mul_nocheck(item, item, prim_poly=prim_poly)
        result = gf_2_4_mul_nocheck(result, item, prim_poly=prim_poly)

    return result


gf_2_4_get_inverse_nocheck = gf_2_4_get_inverse_nocheck_exponential


def gf_2_4_div(a: int, b: int, prim_poly: int = GF_2_4_PRIM_POLY) -> int:
    _gf_2_4_check(a)
    _gf_2_4_check(b)
    _gf_2_4_check_prim_poly(prim_poly)

    if b == 0x0:
        raise ValueError("gf_2_4_div: divide by zero")

    return gf_2_4_div_nocheck(a, b, prim_poly=prim_poly)


def gf_2_4_div_nocheck(a: int, b: int, prim_poly: int = GF_2_4_PRIM_POLY) -> int:
    return gf_2_4_mul_nocheck(a, gf_2_4_get_inverse(b, prim_poly=prim_poly))


def gf_2_4_print_poly(a: int) -> None:
    if a == 0:
        print('0')
        return

    poly_list = []

    for i in range(3, -1, -1):
        if a & (1 << i) == (1 << i):
            if i != 0:
                poly_list.append('x^%d' % i)
            else:
                poly_list.append('1')

    print(' + '.join(poly_list))


# GF(2^8) 的本原多项式为 x^8 + x^4 + x^3 + x + 1
GF_2_8_PRIM_POLY = 0x11b


def _gf_2_8_check_prim_poly(prim_poly: int) -> None:
    # XXX: stub
    pass


def _gf_2_8_check(a: int) -> None:
    # GF(2^8) 中元占 8 位
    if not (0 <= a <= 255):
        raise ValueError("_gf_2_8_check: invalid gf(2^8) element %d" % a)


def gf_2_8_add(a: int, b: int) -> int:
    _gf_2_8_check(a)
    _gf_2_8_check(b)

    return gf_2_8_add_nocheck(a, b)


def gf_2_8_add_nocheck(a: int, b: int) -> int:
    return a ^ b


gf_2_8_sub = gf_2_8_add
gf_2_8_sub_nocheck = gf_2_8_add_nocheck


def _gf_2_4_check_prim_poly(prim_poly: int) -> None:
    # XXX: stub
    pass


def gf_2_8_mul_x_nocheck(a: int, prim_poly: int = GF_2_8_PRIM_POLY) -> int:
    # 看对应的多项式 7 次项是否为 1，需要用位掩码 0x80 判断
    if a & 0x80 == 0x80:
        # 如果对应的多项式 7 次项为 1，那么先异或 0x80 减去最高次项，再左移一位，
        # 然后异或 0x1a (x^4 + x^3 + x + 1)，
        # 这相当于先左移一位再模掉 x^8 + x^4 + x^3 + x + 1
        return ((a ^ 0x80) << 1) ^ (prim_poly & 0xff)
    else:
        # 否则只需要左移一位即可
        return a << 1


def gf_2_8_mul_x(a: int, prim_poly: int = GF_2_8_PRIM_POLY) -> int:
    _gf_2_8_check(a)
    if prim_poly != GF_2_8_PRIM_POLY:
        _gf_2_8_check_prim_poly(prim_poly)

    return gf_2_8_mul_x_nocheck(a, prim_poly=prim_poly)


def gf_2_8_mul(a: int, b: int, prim_poly: int = GF_2_8_PRIM_POLY) -> int:
    _gf_2_8_check(a)
    _gf_2_8_check(b)
    if prim_poly != GF_2_8_PRIM_POLY:
        _gf_2_8_check_prim_poly(prim_poly)

    return gf_2_8_mul_nocheck(a, b, prim_poly=prim_poly)


def gf_2_8_mul_nocheck(a: int, b: int, prim_poly: int = GF_2_8_PRIM_POLY) -> int:
    # GF(2^8) 中的零元是 0x0，这与取哪个多项式做本原多项式无关
    result = 0x0
    a_mul = a

    for i in range(8):
        bitmask = 1 << i

        if b & bitmask == bitmask:
            result = gf_2_8_add_nocheck(result, a_mul)

        a_mul = gf_2_8_mul_x_nocheck(a_mul, prim_poly=prim_poly)

    return result


def gf_2_8_get_inverse(a: int, prim_poly: int = GF_2_8_PRIM_POLY) -> int:
    _gf_2_8_check(a)
    _gf_2_8_check_prim_poly(prim_poly)

    if a == 0x0:
        raise ValueError("gf_2_8_get_inverse: 0x0 has no inverse" % a)

    return gf_2_8_get_inverse_nocheck(a)


_gf_2_8_inverse_lookup_table = \
    [0, 1, 141, 246, 203, 82, 123, 209, 232, 79, 41, 192, 176, 225,
     229, 199, 116, 180, 170, 75, 153, 43, 96, 95, 88, 63, 253, 204,
     255, 64, 238, 178, 58, 110, 90, 241, 85, 77, 168, 201, 193, 10,
     152, 21, 48, 68, 162, 194, 44, 69, 146, 108, 243, 57, 102, 66,
     242, 53, 32, 111, 119, 187, 89, 25, 29, 254, 55, 103, 45, 49,
     245, 105, 167, 100, 171, 19, 84, 37, 233, 9, 237, 92, 5, 202,
     76, 36, 135, 191, 24, 62, 34, 240, 81, 236, 97, 23, 22, 94,
     175, 211, 73, 166, 54, 67, 244, 71, 145, 223, 51, 147, 33, 59,
     121, 183, 151, 133, 16, 181, 186, 60, 182, 112, 208, 6, 161, 250,
     129, 130, 131, 126, 127, 128, 150, 115, 190, 86, 155, 158, 149,
     217, 247, 2, 185, 164, 222, 106, 50, 109, 216, 138, 132, 114, 42,
     20, 159, 136, 249, 220, 137, 154, 251, 124, 46, 195, 143, 184,
     101, 72, 38, 200, 18, 74, 206, 231, 210, 98, 12, 224, 31, 239, 17,
     117, 120, 113, 165, 142, 118, 61, 189, 188, 134, 87, 11, 40, 47,
     163, 218, 212, 228, 15, 169, 39, 83, 4, 27, 252, 172, 230, 122, 7,
     174, 99, 197, 219, 226, 234, 148, 139, 196, 213, 157, 248, 144,
     107, 177, 13, 214, 235, 198, 14, 207, 173, 8, 78, 215, 227, 93,
     80, 30, 179, 91, 35, 56, 52, 104, 70, 3, 140, 221, 156, 125, 160,
     205, 26, 65, 28]


def gf_2_8_get_inverse_nocheck_lookup_table(a: int, prim_poly: int = GF_2_8_PRIM_POLY) -> int:
    # 实际上 _gf_2_8_inverse_lookup_table[0] 没用
    return _gf_2_8_inverse_lookup_table[a]


def gf_2_8_get_inverse_nocheck_exponential(a: int, prim_poly: int = GF_2_8_PRIM_POLY) -> int:
    # 对于 GF(2^8) 中任一非零元 g，它的逆元一定是它的 2^8 - 2 = 254 次方
    # 这可以通过指数的性质得以证明

    # GF(2^8) 中的单位元是 0x1，这与取哪个多项式做本原多项式无关
    result = 0x1

    # 重复 7 遍平方和加法运算，即可算出任一元的 254 次方
    # 先令要加的项为 a, 再重复三遍先把单独一项平方，然后乘到结果上的操作
    # 这样也能避免侧信道攻击
    item = a

    for i in range(7):
        item = gf_2_8_mul_nocheck(item, item, prim_poly=prim_poly)
        result = gf_2_8_mul_nocheck(result, item, prim_poly=prim_poly)

    return result


gf_2_8_get_inverse_nocheck = gf_2_8_get_inverse_nocheck_exponential


def gf_2_8_div(a: int, b: int, prim_poly: int = GF_2_8_PRIM_POLY) -> int:
    _gf_2_8_check(a)
    return gf_2_8_div_nocheck(a, b, prim_poly=prim_poly)


def gf_2_8_div_nocheck(a: int, b: int, prim_poly: int = GF_2_8_PRIM_POLY) -> int:
    return gf_2_8_mul_nocheck(a, gf_2_4_get_inverse(b, prim_poly=prim_poly))


def gf_2_8_print_poly(a: int) -> None:
    if a == 0:
        print('0')
        return

    poly_list = []

    for i in range(7, -1, -1):
        if a & (1 << i) == (1 << i):
            if i != 0:
                poly_list.append('x^%d' % i)
            else:
                poly_list.append('1')

    print(' + '.join(poly_list))
