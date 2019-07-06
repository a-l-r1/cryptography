from lll import *
from lll import _gram_schmidt, _LLLVector, _LLLMatrix


def main() -> None:
    print(_LLLVector([1, 2, 3]).dot_product(_LLLVector([4, 5, 6])))
    print(_LLLVector([1, 1, 1]).projection(_LLLVector([-1, 0, 2])))
    print(_LLLVector([1, 1, 1]).projection_vector(_LLLVector([-1, 0, 2])))
    print(_LLLVector([1, 2, 3]) - _LLLVector([6, 5, 4]))
    print(_LLLVector(["3/2", "4/5", "1/4"]) * 2)
    print(_LLLVector([42, 42, 42]))

    print(_gram_schmidt([_LLLVector([3, 1]), _LLLVector([2, 2])]))
    print(_gram_schmidt([_LLLVector([4, 1, 2]), _LLLVector([4, 7, 2]), _LLLVector([3, 1, 7])]))

    print(lll([[1, 1, 1], [-1, 0, 2], [3, 5, 6]], 0.75))
    print(lll([[105, 821, 404, 328], [881, 667, 644, 927], [181, 483, 87, 500], [893, 834, 732, 441]], 0.75))
    print(lll([[1, 1, 1], [-1, 0, 2], [3, 5, 6]], 0.75))
    print(lll([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [575, 436, 1586, 1030, 1921, 569, 721, 1183, 1570, -6665]], 0.4))

    m = [[0 for _ in range(10)] for _ in range(10)]
    for i in range(0, 10 - 1):
        m[i][i] = 1
    pk = [575, 436, 1586, 1030, 1921, 569, 721, 1183, 1570]
    ct = 6665
    for i in range(len(pk)):
        m[i][10 - 1] = pk[i]
    m[10 - 1][10 - 1] = -ct
    print(m)
    delta = 0.75
    intermediate = lll(m, delta)
    print(intermediate)


if __name__ == '__main__':
    main()