import functools
import itertools
from typing import List, Iterable

import finite_field

aes_block_length = 128
_aes_cbc_iv = bytes.fromhex('0123456789abcdef0123456789abcdef')


class AESState(object):
    _nb_dict = {128: 4}

    _aes_column_length = 4

    _nb_round_count_dict = {
        4: 10
    }

    _bytesub_table = [
        99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118,
        202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192,
        183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21,
        4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117,
        9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132,
        83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207,
        208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168,
        81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210,
        205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115,
        96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219,
        224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121,
        231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8,
        186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138,
        112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158,
        225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223,
        140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22
    ]

    _bytesub_inv_table = [
        82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251,
        124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203,
        84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78,
        8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37,
        114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146,
        108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132,
        144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6,
        208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107,
        58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115,
        150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110,
        71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27,
        252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244,
        31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95,
        96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239,
        160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97,
        23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125
    ]

    _nb_shiftrow_dict = {
        4: [0, 1, 2, 3]
    }

    _nb_invshiftrow_dict = {
        4: [0, 3, 2, 1]
    }

    _mixcolumn_matrix = [
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02]
    ]

    _invmixcolumn_matrix = [
        [0x0e, 0x0b, 0x0d, 0x09],
        [0x09, 0x0e, 0x0b, 0x0d],
        [0x0d, 0x09, 0x0e, 0x0b],
        [0x0b, 0x0d, 0x09, 0x0e]
    ]

    def __init__(self, b):
        length = len(b)

        if length * 8 not in self._nb_dict:
            raise ValueError(__name__ + ": invalid bytes length")

        self.nb = self._nb_dict[length * 8]
        self.row_length = len(b) // 4
        self.data = [bytearray(b[i:i + 4]) for i in range(0, length, self.row_length)]

    _str_header = "AESState(\n"
    _str_footer = "\n)"

    def __str__(self):
        result = ""
        result += self._str_header

        result += "length = %d, nb = %d, row_length = %d\n" % (self.nb * self.row_length, self.nb, self.row_length)
        result += '\n'.join(map(lambda x: ' '.join(map(lambda y: y.to_bytes(1, 'little').hex(), x)), zip(*self.data)))

        result += self._str_footer
        return result

    def get_round_count(self) -> int:
        if self.nb not in self._nb_dict.values():
            raise ValueError(__name__ + ": invalid nb")

        return self._nb_round_count_dict[self.nb]

    @classmethod
    def bytesub_single_byte(cls, i: int) -> int:
        return cls._bytesub_table[i]

    @classmethod
    def invbytesub_single_byte(cls, i: int) -> int:
        return cls._bytesub_inv_table[i]

    def bytesub(self) -> None:
        self.data = list(map(lambda x: bytearray(self.bytesub_single_byte(i) for i in x), self.data))

    def invbytesub(self) -> None:
        self.data = list(map(lambda x: bytearray(self.invbytesub_single_byte(i) for i in x), self.data))

    def _left_rshift_row(self, row_index: int, shift_count: int) -> None:
        curr_row_list = list(map(lambda x: x[row_index], self.data))
        curr_row_list = curr_row_list[shift_count:] + curr_row_list[:shift_count]

        for i in range(len(curr_row_list)):
            self.data[i][row_index] = curr_row_list[i]

    def shiftrow(self) -> None:
        if self.nb not in self._nb_dict.values():
            raise ValueError(__name__ + ": invalid nb")

        if self.nb == 4:
            for i in range(len(self.data)):
                self._left_rshift_row(i, self._nb_shiftrow_dict[self.nb][i])

            return

    def invshiftrow(self) -> None:
        if self.nb not in self._nb_dict.values():
            raise ValueError(__name__ + ": invalid nb")

        if self.nb == 4:
            for i in range(len(self.data)):
                self._left_rshift_row(i, self._nb_invshiftrow_dict[self.nb][i])

    @classmethod
    def mixcolumn_single_column(cls, column: bytearray) -> bytearray:
        if len(column) != cls._aes_column_length:
            raise ValueError(__name__ + ": column length != %d" % cls._aes_column_length)

        result = bytearray(cls._aes_column_length)

        for i in range(cls._aes_column_length):
            result[i] = functools.reduce(finite_field.gf_2_8_add,
                                         map(finite_field.gf_2_8_mul, column, cls._mixcolumn_matrix[i]))

        return result

    @classmethod
    def invmixcolumn_single_column(cls, column: bytearray) -> bytearray:
        if len(column) != cls._aes_column_length:
            raise ValueError(__name__ + ": column length != %d" % cls._aes_column_length)

        result = bytearray(cls._aes_column_length)

        for i in range(cls._aes_column_length):
            result[i] = functools.reduce(finite_field.gf_2_8_add,
                                         map(finite_field.gf_2_8_mul, column, cls._invmixcolumn_matrix[i]))

        return result

    def mixcolumn(self) -> None:
        for i in range(len(self.data)):
            self.data[i] = self.mixcolumn_single_column(self.data[i])

    def invmixcolumn(self) -> None:
        for i in range(len(self.data)):
            self.data[i] = self.invmixcolumn_single_column(self.data[i])

    def addroundkey(self, round_key: List[bytearray]) -> None:
        # TODO: key length != 128 || pt length != 128
        if len(round_key) != 4:
            raise ValueError(__name__ + ": invalid round key length")

        if self.nb not in self._nb_dict.values():
            raise ValueError(__name__ + ": invalid state")

        for i in range(len(self.data)):
            self.data[i] = bytearray(a ^ b for a, b in zip(self.data[i], round_key[i]))

    def to_bytes(self) -> bytes:
        return bytes(itertools.chain.from_iterable(self.data))


class AESKeyState(AESState):
    def __init__(self, b):
        super(AESKeyState, self).__init__(b)

    _str_header = "AESKeyState(\n"

    def __str__(self) -> str:
        return super(AESKeyState, self).__str__()

    _aes_round_constant_table = [
        bytes.fromhex('01000000'),
        bytes.fromhex('02000000'),
        bytes.fromhex('04000000'),
        bytes.fromhex('08000000'),
        bytes.fromhex('10000000'),
        bytes.fromhex('20000000'),
        bytes.fromhex('40000000'),
        bytes.fromhex('80000000'),
        bytes.fromhex('1B000000'),
        bytes.fromhex('36000000')
    ]

    @classmethod
    def _g(cls, k: bytearray, round_: int) -> bytearray:
        # 做 k 的一份拷贝
        k = bytearray(k)
        k[0], k[1], k[2], k[3] = k[1], k[2], k[3], k[0]

        k = bytearray(map(lambda x: AESState.bytesub_single_byte(x), k))
        k = bytearray(i ^ j for (i, j) in zip(cls._aes_round_constant_table[round_], k))

        return k

    def _iter_key(self, rounds: int) -> Iterable[List[bytearray]]:
        # 第一次迭代
        # TODO: 密钥长度 != 128 bit
        yield self.data

        old_result = self.data
        result = [bytearray() for _ in range(4)]

        for i in range(rounds):
            result[0] = bytearray(x ^ y for (x, y) in zip(self._g(old_result[3], i), old_result[0]))
            result[1] = bytearray(x ^ y for (x, y) in zip(result[0], old_result[1]))
            result[2] = bytearray(x ^ y for (x, y) in zip(result[1], old_result[2]))
            result[3] = bytearray(x ^ y for (x, y) in zip(result[2], old_result[3]))

            old_result = result
            result = [bytearray() for _ in range(4)]

            yield old_result

        return

    def gen_key_list(self) -> List[List[bytearray]]:
        # TODO: key size != 128 bit || pt size != 128 bit
        result = list(self._iter_key(10))
        return result


def encrypt(p: bytes, k: bytes) -> bytes:
    state = AESState(p)
    key_state = AESKeyState(k)
    key_list = key_state.gen_key_list()
    round_count = key_state.get_round_count()

    state.addroundkey(key_list[0])

    for i in range(round_count - 1):
        state.bytesub()
        state.shiftrow()
        state.mixcolumn()
        state.addroundkey(key_list[i + 1])

    state.bytesub()
    state.shiftrow()
    state.addroundkey(key_list[round_count])

    return state.to_bytes()


def decrypt(c: bytes, k: bytes) -> bytes:
    state = AESState(c)
    key_state = AESKeyState(k)
    key_list = key_state.gen_key_list()
    round_count = key_state.get_round_count()

    state.addroundkey(key_list[round_count])
    
    for i in range(round_count - 2, 0 - 1, -1):
        state.invbytesub()
        state.invshiftrow()
        state.invmixcolumn()
        state.addroundkey(list(map(AESState.invmixcolumn_single_column, key_list[i + 1])))

    state.invbytesub()
    state.invshiftrow()
    state.addroundkey(key_list[0])

    return state.to_bytes()


def encrypt_file(p_path: str, c_path: str, k: bytes) -> None:
    fi = open(p_path, 'rb')
    fo = open(c_path, 'wb')

    last_ciphertext_bytes = _aes_cbc_iv

    while True:
        curr_bytes = fi.read(aes_block_length // 8)

        if len(curr_bytes) == 0:
            break

        if len(curr_bytes) < aes_block_length // 8:
            curr_bytes = curr_bytes + bytes(aes_block_length // 8 - len(curr_bytes))

        curr_bytes = bytes(a ^ b for a, b in zip(curr_bytes, last_ciphertext_bytes))
        ciphertext_bytes = encrypt(curr_bytes, k)
        fo.write(ciphertext_bytes)

        last_ciphertext_bytes = ciphertext_bytes

    fi.close()
    fo.close()


def decrypt_file(p_path: str, c_path: str, k: bytes) -> None:
    fi = open(c_path, 'rb')
    fo = open(p_path, 'wb')

    last_ciphertext_bytes = _aes_cbc_iv

    while True:
        curr_bytes = fi.read(aes_block_length // 8)

        if len(curr_bytes) == 0:
            break

        if len(curr_bytes) < aes_block_length // 8:
            curr_bytes = curr_bytes + bytes(aes_block_length // 8 - len(curr_bytes))

        plaintext_bytes = decrypt(curr_bytes, k)
        plaintext_bytes = bytes(a ^ b for a, b in zip(plaintext_bytes, last_ciphertext_bytes))
        fo.write(plaintext_bytes)

        last_ciphertext_bytes = curr_bytes

    fi.close()
    fo.close()
