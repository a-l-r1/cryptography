import gcd
import letter
import modular_matrix


def _check_key(k: modular_matrix.ModularMatrix, letter_set: set):
    if k.rows != k.columns:
        raise ValueError("_check_key: key is not a square matrix")

    n_l = len(letter_set)

    if k.modulus != n_l:
        raise ValueError("_check_key: key modulus != letter set size")

    d = k.det()
    if gcd.gcd(d, n_l) != 1:
        raise ValueError("_check_key: key determinant not coprime with letter set size")


def _check_plaintext(s: str, letter_set: set) -> None:
    if any(map(lambda x: x not in letter_set, s)):
        raise ValueError("_check_plaintext: s has letter(s) not in letter set")


def _check_plaintext_ciphertext_pair_length(c: str, p: str) -> None:
    if len(c) != len(p):
        raise ValueError("_check_plaintext_ciphertext_pair_length: plaintext and ciphertext not of equal length")


def _check_chunk_length(c_chunks: list, p_chunks: list, m: int):
    if len(c_chunks[-1]) != m:
        raise ValueError("_check_ciphertext_chunk_length: last chunk of ciphertext not padded")

    if len(p_chunks[-1]) != m:
        raise ValueError("_check_ciphertext_chunk_length: last chunk of plaintext not padded")

    if len(c_chunks) < m:
        raise ValueError("_check_ciphertext_chunk_length: number of ciphertext chunks < m")


def encrypt(p: str, k: modular_matrix.ModularMatrix, letter_set: set = letter.LETTER_SET) -> str:
    _check_key(k, letter_set)
    _check_plaintext(p, letter_set)

    return encrypt_nocheck(p, k)


def encrypt_nocheck(p: str, k: modular_matrix.ModularMatrix) -> str:
    m = k.rows

    _padding = 'X'
    p += _padding * (-len(p) % m)
    p = p.upper()

    p_groups = [p[i: i + m] for i in range(0, len(p), m)]

    result = ''.join(map(lambda x: ''.join(map(lambda y: chr(y + letter.ORD_BASE_CAPITAL_A),
                                               k * modular_matrix.ModularMatrix(m, 1, map(
                                                   lambda z: ord(z) - letter.ORD_BASE_CAPITAL_A, x)))), p_groups))

    return result


def decrypt(c: str, k: modular_matrix.ModularMatrix, letter_set: set = letter.LETTER_SET) -> str:
    _check_key(k, letter_set)
    _check_plaintext(c, letter_set)

    return decrypt_nocheck(c, k)


def decrypt_nocheck(c: str, k: modular_matrix.ModularMatrix) -> str:
    k_d = k.inv()

    return encrypt_nocheck(c, k_d)


def get_key(c: str, p: str, m: int, modulus: int = letter.LETTER_COUNT) -> modular_matrix.ModularMatrix:
    _check_plaintext_ciphertext_pair_length(c, p)

    c = c.upper()
    p = p.upper()

    c_chunks = [c[i: i + m] for i in range(0, len(c), m)]
    p_chunks = [p[i: i + m] for i in range(0, len(p), m)]

    _check_chunk_length(c_chunks, p_chunks, m)

    curr_c = modular_matrix.ModularMatrix(m, m, modulus=modulus)
    curr_p = modular_matrix.ModularMatrix(m, m, modulus=modulus)

    c_chunks_iter = iter(c_chunks)
    p_chunks_iter = iter(p_chunks)

    for i in range(m):
        curr_c_chunk = next(c_chunks_iter)
        curr_p_chunk = next(p_chunks_iter)

        for j in range(m):
            curr_c[m * i + j] = ord(curr_c_chunk[j]) - letter.ORD_BASE_CAPITAL_A
            curr_p[m * i + j] = ord(curr_p_chunk[j]) - letter.ORD_BASE_CAPITAL_A

    # XXX: 比滑动窗口算法更好的算法
    curr_column = 0

    while True:
        try:
            curr_p_inv = curr_p.inv()
            curr_c_column = modular_matrix.ModularMatrix(m, 1, modulus=modulus)
            result = modular_matrix.ModularMatrix(m, m, modulus=modulus)

            for i in range(m):
                curr_c_column[:] = curr_c[i: len(curr_c): m]
                result[i * m: i * m + m] = curr_p_inv @ curr_c_column

            return result
        except ValueError:
            try:
                curr_c_chunk = next(c_chunks_iter)
                curr_p_chunk = next(p_chunks_iter)
            except StopIteration:
                raise ValueError("get_key: all text pairs tried but no success")

            for i in range(m):
                for letter_index in range(m):
                    curr_c[i * m + curr_column] = ord(curr_c_chunk[letter_index]) - letter.ORD_BASE_CAPITAL_A
                    curr_p[i * m + curr_column] = ord(curr_p_chunk[letter_index]) - letter.ORD_BASE_CAPITAL_A

            curr_column += 1

            # curr_column 总是 == curr_p_column
            if curr_column == m:
                curr_column = 0


def main() -> None:
    k = get_key('PQCFKU', 'FRIDAY', 2)
    print(encrypt('FRIDAY', k))


if __name__ == '__main__':
    main()
