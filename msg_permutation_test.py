from msg_permutation import *


def main() -> None:
    # xkcd #936
    m = b'correct horse battery staple'

    permutations = get_permutation_list(m, 10)
    print(permutations)

    sample = [b'correct \x08 horse battery staple',
              b'correct horse \x08 battery staple',
              b'correct horse battery \x08 staple',
              b'correct \x08 \x08 horse \x08 battery \x08 staple',
              b'correct \x08 horse \x08 \x08 battery \x08 staple',
              b'correct \x08 horse \x08 battery \x08 \x08 staple',
              b'correct \x08 \x08 \x08 horse \x08 \x08 battery \x08 \x08 staple',
              b'correct \x08 \x08 horse \x08 \x08 \x08 battery \x08 \x08 staple',
              b'correct \x08 \x08 horse \x08 \x08 battery \x08 \x08 \x08 staple',
              b'correct \x08 \x08 \x08 \x08 horse \x08 \x08 \x08 battery \x08 \x08 \x08 staple',
              b'correct \x08 \x08 \x08 horse \x08 \x08 \x08 \x08 battery \x08 \x08 \x08 staple']
    print(permutations == sample)


if __name__ == '__main__':
    main()
