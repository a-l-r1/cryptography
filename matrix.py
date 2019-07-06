import operator
from typing import Sequence


class Matrix(list):
    def __init__(self, *args, default_value: object = 0):
        super().__init__()

        if 1 <= len(args) <= 3:
            rows = int(args[0])
            if len(args) == 1:
                columns = int(args[0])
            else:
                columns = int(args[1])

            self.rows = rows
            self.columns = columns

            if len(args) == 1 or len(args) == 2:
                self.extend([default_value for _ in range(rows * columns)])

            if len(args) == 3:
                iterable = args[2]
                if hasattr(iterable, '__len__'):
                    if len(iterable) != rows * columns:
                        raise TypeError("Matrix(): iterable size mismatch")

                self.extend(iterable)

            return

        raise TypeError("Matrix() takes at most 3 positional arguments, %d given" % len(args))

    def __add__(self, other: Sequence):
        if len(other) == 1:
            return Matrix(self.rows, self.columns, map(operator.add, self, other))
        else:
            if len(other) != len(self):
                raise TypeError("cannot add sequence of different length")

            return Matrix(self.rows, self.columns, map(operator.add, self, other))

    def __sub__(self, other: Sequence):
        if len(other) == 1:
            return Matrix(self.rows, self.columns, map(operator.add, self, other))
        else:
            if len(other) != len(self):
                raise TypeError("cannot subtract sequence of different length")

            return Matrix(self.rows, self.columns, map(operator.sub, self, other))

    def __iadd__(self, other: Sequence):
        if len(other) == 1:
            for i in range(len(self)):
                self[i] += other

            return self
        else:
            if len(other) != len(self):
                raise TypeError("cannot add sequence of different length")

            for i in range(len(self)):
                self[i] += other[i]

            return self

    def __isub__(self, other: Sequence):
        if len(other) == 1:
            for i in range(len(self)):
                self[i] -= other

            return self
        else:
            if len(other) != len(self):
                raise TypeError("cannot add sequence of different length")

            for i in range(len(self)):
                self[i] -= other[i]

            return self

    def __mul__(self, other):
        if len(other) == 1:
            return Matrix(self.rows, self.columns, map(operator.mul, self, other))
        else:
            if type(other) != type(self):
                raise TypeError("cannot multiply non-Matrix")

            if other.rows != self.columns:
                raise TypeError("rows of the right matrix != columns of this matrix")

            result = Matrix(self.rows, other.columns)

            for i in range(self.rows):
                for j in range(other.columns):
                    for k in range(self.columns):
                        result[i * result.columns + j] += self[i * self.columns + k] * other[k * other.columns + j]

        return result

    __matmul__ = __mul__

    # XXX: 写一个更高效的自乘算法
    def __imul__(self, other):
        if len(other) == 1:
            for i in range(len(self)):
                self[i] *= other

            return self
        else:
            self_orig = Matrix(self.rows, self.columns, self)

            if type(other) != type(self):
                raise TypeError("cannot multiply non-Matrix")

            if other.rows != self.columns:
                raise TypeError("rows of the right matrix != columns of this matrix")

            for i in range(self.rows):
                for j in range(other.columns):
                    self[i * self.rows + j] = 0

                    for k in range(self.columns):
                        self[i * self.rows + j] += self_orig[i * self.rows + k] * other[k * other.rows + j]

        return self

    __imatmul__ = __imul__

    _str_header = 'Matrix(\n'
    _str_footer = '\n)'

    def __str__(self):
        return self._str_header + '\n'.join(map(lambda x: str(self[x: x + self.columns]),
                                                range(0, len(self), self.columns))) + self._str_footer

    def get_element(self, i: int, j: int):
        return super().__getitem__(i * self.columns + j)

    def get_inverse(self):
        raise NotImplemented

    def det(self):
        if self.columns != self.rows:
            raise ValueError("not a square matrix")

        if self.rows == 1:
            return self[0]

        if self.rows == 2:
            return self[0] * self[3] - self[1] * self[2]

        result = 0
        # 预先分配内存以提高效率
        new_matrix = Matrix(self.columns - 1, self.rows - 1)

        for column in range(self.columns):
            for i in range(1, self.rows):
                new_row = i - 1

                for j in range(self.columns):
                    if j == column:
                        continue
                    elif j < column:
                        new_column = j
                    else:
                        new_column = j - 1

                    new_matrix[new_row * new_matrix.rows + new_column] = self[i * self.rows + j]

            if column % 2 == 0:
                result += self[column] * new_matrix.det()
            else:
                result -= self[column] * new_matrix.det()

        return result
