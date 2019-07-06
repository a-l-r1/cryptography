LETTER_COUNT = 26

ORD_BASE_SMALL_A = ord('a')
ORD_BASE_CAPITAL_A = ord('A')

LETTER_SET = {chr(i) for i in range(ORD_BASE_CAPITAL_A, ORD_BASE_CAPITAL_A + LETTER_COUNT)}
ASCII_LETTER_SET = {chr(i) for i in range(ORD_BASE_CAPITAL_A, 127+1)}

LETTER_FREQ_DICT = {'E': 0.12702, 'T': 0.09056, 'A': 0.08167, 'O': 0.07507, 'I': 0.06966, 'N': 0.06749, 'S': 0.06327,
                    'H': 0.06094, 'R': 0.05987, 'D': 0.04253, 'L': 0.04025, 'C': 0.02782, 'U': 0.02758, 'M': 0.02406,
                    'W': 0.02360, 'F': 0.02228, 'G': 0.02015, 'Y': 0.01974, 'P': 0.01929, 'B': 0.01492, 'V': 0.00978,
                    'K': 0.00772, 'J': 0.00153, 'X': 0.00150, 'Q': 0.00095, 'Z': 0.00074}

LETTER_FREQ_LIST = list('ETAOINSHRDLCUMWFGYPBVKJXQZ')


def strip_whitespace(c: str) -> str:
    return c.replace(' ', '')
