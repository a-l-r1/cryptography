import vigenere

def _check_key(k: int) -> None:
    if k < 0 or k > 25:
        raise ValueError("_check_key: key < 0 or key > 25")

def encrypt(s: str, k: int) -> str:
    _check_key(k)
    
    return vigenere.encrypt(s, chr(k + vigenere.ORD_BASE_SMALL_A))

def encrypt_nocheck(s: str, k: int) -> str:
    return vigenere.encrypt_nocheck(s, \
        chr(k + vigenere.ORD_BASE_SMALL_A))
