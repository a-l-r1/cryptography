import numbers
import copy
from decimal import Decimal


class EC(object):
    def __init__(self, a, b):
        if a.__class__ != b.__class__:
            raise ValueError("__init__: a and b is of different classes")

        if a.__class__(4) * a * a * a + a.__class__(27) * b * b == a.__class__(0):
            raise ValueError("__init__: 4 * a^3 + 27 * b^2 == 0")

        self.a = a
        self.b = b
        self.number_class = a.__class__

    def __str__(self):
        _header = 'EC('
        _template = 'number_class=%s, a=%s, b=%s'
        _footer = ')'

        return _header + _template % (self.number_class.__qualname__, str(self.a), str(self.b)) + _footer

    def __eq__(self, other):
        if not isinstance(other, EC):
            return False

        return self.a == other.a and self.b == other.b and self.number_class == other.number_class


class ECPoint(object):
    _infinite_tag = 'infinite'

    def __init__(self, ec: EC, *args):
        super(ECPoint, self).__init__()

        if len(args) > 2 or len(args) == 0:
            raise TypeError("__init__() takes 2 positional arguments but %d were given" % len(args))

        if len(args) == 1:
            if not isinstance(args[0], str):
                raise TypeError("__init__: arg 1 must be str")

            if args[0] != self._infinite_tag:
                raise ValueError('desc must be\'infinite\'')

            self.ec = ec
            self.is_infinite = True

        if len(args) == 2:
            if args[0].__class__ != args[1].__class__:
                raise TypeError("__init__: x and y is of different types")

            self.x = args[0]
            self.y = args[1]
            self.ec = ec
            self.is_infinite = False

    def __str__(self) -> str:
        _str_header = 'ECPoint('
        _content_template = 'x=%s, y=%s, ec=%s'
        _content_template_infinite = 'infinite, ec=%s'
        _str_footer = ')'

        if self.is_infinite:
            return _str_header + _content_template_infinite % (str(self.ec),) + _str_footer
        else:
            return _str_header + _content_template % (str(self.x), str(self.y), str(self.ec)) + _str_footer

    def __eq__(self, other) -> bool:
        if not isinstance(other, ECPoint):
            return False

        if self.is_infinite:
            return other.is_infinite
        else:
            return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash(str(self))

    def __add__(self, other):
        if not isinstance(other, ECPoint):
            return NotImplemented

        if self.ec != other.ec:
            raise ValueError("__add__: different ECCs")

        if self.is_infinite and other.is_infinite:
            return ECPoint(self.ec, 'infinite')

        if self.is_infinite:
            return ECPoint(self.ec, other.x, other.y)

        if other.is_infinite:
            return ECPoint(self.ec, self.x, self.y)

        result = ECPoint(self.ec, self.x.__class__(0), self.x.__class__(0))

        if self.x != other.x:
            delta = (other.y - self.y) / (other.x - self.x)

            result.x = delta * delta - self.x - other.x
            result.y = -self.y + delta * (self.x - result.x)
        else:
            if self.y == other.y:
                intermediate = (self.x.__class__(3) * self.x * self.x + self.ec.a) / \
                               (self.x.__class__(2) * self.y)

                result.x = intermediate * intermediate - self.x.__class__(2) * self.x
                result.y = intermediate * (self.x - result.x) - self.y
            else:
                result = ECPoint(self.ec, 'infinite')

        return result

    def __neg__(self):
        if self.is_infinite:
            return ECPoint(self.ec, 'infinite')
        else:
            return ECPoint(self.ec, self.x, -self.y)

    def __mul__(self, other):
        return NotImplemented

    def __rmul__(self, other):
        if not isinstance(other, numbers.Integral):
            return NotImplemented

        other = int(other)

        if other == 0:
            return ECPoint(self.ec, 'infinite')

        if other < 0:
            raise ValueError("__mul__: coefficient < 0")

        if other == 1:
            return ECPoint(self.ec, self.x, self.y)

        if other == 2:
            return self + self

        bit_list = list(bin(other)[2:])
        result = ECPoint(self.ec, 'infinite')
        curr_item = None

        for bit in reversed(bit_list):
            if curr_item is None:
                # TODO: deepcopy too long?
                curr_item = copy.deepcopy(self)
            else:
                curr_item = 2 * curr_item

            if bit == '1':
                result += curr_item

        return result
