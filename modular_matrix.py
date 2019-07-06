import gcd
import letter
import matrix


class ModularMatrix(matrix.Matrix):
    def __init__(self, *args, default_value: int = 0, modulus: int = letter.LETTER_COUNT):
        super().__init__(*args, default_value=default_value)

        if modulus == 0:
            raise ValueError("ModularMatrix() cannot be initialized with modulus 0")

        self.modulus = modulus
        for i in range(len(self)):
            self[i] %= self.modulus

        self._str_header = "ModularMatrix() (modulus %d) (\n" % self.modulus

        return

    def __add__(self, other):
        return ModularMatrix(self.rows, self.columns, map(lambda x: x % self.modulus, super().__add__(other)))

    def __sub__(self, other):
        return ModularMatrix(self.rows, self.columns, map(lambda x: x % self.modulus, super().__sub__(other)))

    def __iadd__(self, other):
        super().__iadd__(other)

        for i in range(len(self)):
            self[i] %= self.modulus

        return self

    def __isub__(self, other):
        super().__isub__(other)

        for i in range(len(self)):
            self[i] %= self.modulus

        return self

    def __mul__(self, other):
        return ModularMatrix(self.rows, self.columns, map(lambda x: x % self.modulus, super().__mul__(other)))

    __matmul__ = __mul__

    def __imul__(self, other):
        super().__imul__(other)

        for i in range(len(self)):
            self[i] %= self.modulus

        return self

    __imatmul__ = __imul__

    def det(self):
        return super().det() % self.modulus

    def inv(self):
        d = self.det()

        if gcd.gcd(d, self.modulus) != 1:
            raise ValueError("not reversible under modulus %d" % self.modulus)

        d_inv = gcd.get_modular_inverse(d, self.modulus)

        if self.rows == 1:
            return ModularMatrix(self.rows, self.columns, [self[0]], modulus=self.modulus)

        new_matrix = ModularMatrix(self.rows - 1, self.columns - 1, modulus=self.modulus)
        result = ModularMatrix(self.rows, self.columns, modulus=self.modulus)

        for i in range(self.rows):
            for j in range(self.columns):
                for new_row in range(self.rows):
                    if new_row == i:
                        continue
                    elif new_row > i:
                        target_row = new_row - 1
                    else:
                        target_row = new_row

                    for new_column in range(self.columns):
                        if new_column == j:
                            continue
                        elif new_column > j:
                            target_column = new_column - 1
                        else:
                            target_column = new_column

                        new_matrix[target_row * new_matrix.rows + target_column] = \
                            self[new_row * self.rows + new_column]

                result[j * self.rows + i] = d_inv * (-1) ** (i + j) * new_matrix.det() % self.modulus

        return result
