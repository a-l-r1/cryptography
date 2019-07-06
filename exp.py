def square_exp(x:int, power:int) -> int:
    if (power < 0):
        raise ValueError("exp: power < 0 is unsupported")
    
    result = 1
	
    bit_list = []
    while (power != 0):
        bit_list.insert(0, power % 2)
        power //= 2

    for i in bit_list:
        result = result * result

        if (i == 1):
            result = result * x

    return result

exp = square_exp
