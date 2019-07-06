import operator, functools

import gcd

def _crt(target:list, modulus:list) -> int:
    m = functools.reduce(operator.mul, modulus)
    
    M = list(map(lambda a: m // a, modulus))
    M_apos = list(map(gcd.get_modular_inverse, M, modulus))
    items = list(map(lambda a, b, c: (a * b * c) % m, M_apos, M, \
        target))
    
    result = functools.reduce(lambda a, b: (a + b) % m, items)
    return result

def _crt_checklength(target:list, modulus:list):
    if (len(target) != len(modulus)):
        raise ValueError("crt: len(target) != len(modulus)")
    if (len(target) == 1):
        raise ValueError("crt: just one equation?")

def _crt_checktype(target:list, modulus:list):
    for i in target:
        if (type(i) != type(0)):
            raise ValueError("crt: %s in target is not int" % str(i))

    for i in modulus:
        if (type(i) != type(0)):
            raise ValueError("crt: %s in modulus is not int" % str(i))

def _crt_checkcoprime(target:list, modulus:list):
    modulus_gcd = functools.reduce(gcd.gcd, modulus)
    
    if (modulus_gcd != 1):
        raise ValueError("crt: modulus not coprime: %s, %s" % \
            (str(target), str(modulus)))

def crt_nocheck(target:list, modulus:list) -> int:
    _crt_checklength(target, modulus)
    
    return _crt(target, modulus)

def crt_nochecktype(target:list, modulus:list) -> int:
    _crt_checklength(target, modulus)
    _crt_checkcoprime(target, modulus)
    
    return _crt(target, modulus)

def crt(target:list, modulus:list) -> int:
    _crt_checklength(target, modulus)
    _crt_checktype(target, modulus)
    _crt_checkcoprime(target, modulus)
    
    return _crt(target, modulus)
