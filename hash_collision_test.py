from hash_collision import *


def main() -> None:
    collision_example = find_collision_pair(gen_rand_bytes, hash_)
    print('%s: %s' % (collision_example[0].hex(), hash_(collision_example[0]).hex()))
    print('%s: %s' % (collision_example[1].hex(), hash_(collision_example[1]).hex()))
    print(hash_(collision_example[0]) == hash_(collision_example[1]))


if __name__ == '__main__':
    main()