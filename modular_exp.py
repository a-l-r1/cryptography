def square_modular_exp(x:int, power:int, modulus:int) -> int:
	if (modulus <= 0):
		raise ValueError("modular_pow: modulus must be " + \
			"positive: (%d ** %d) %% %d" % (x, power, modulus))
	
	result = 1
	
	bit_list = []
	while (power != 0):
		bit_list.insert(0, power % 2)
		power //= 2
	
	for i in bit_list:
		result = (result * result) % modulus
		
		if (i == 1):
			result = (result * x) % modulus
        
	return result

modular_exp = square_modular_exp

def generic_modular_exp(x:int, power:int, modulus:int) -> int:
	if (modulus <= 0):
		raise ValueError("modular_pow: modulus must be " + \
			"positive: (%d ** %d) %% %d" % (x, power, modulus))
	
	result = 1
	
	for i in range(power):
		result = (result * x) % modulus
	
	return result

