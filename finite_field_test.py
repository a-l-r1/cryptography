from finite_field import *


def main() -> None:
    a = GF2Power31(42)
    print(a)

    fp = get_prime_finite_field_element_class(5, 'fp')

    fpn = get_prime_finite_field_power_element_class(3, [fp(1), fp(3), fp(4), fp(2)], 'fpn')

    a = fpn([fp(1), fp(2), fp(3)])
    b = fpn([fp(2), fp(3), fp(2)])
    print(a)
    print(b)
    print(a * b)


if __name__ == '__main__':
    main()