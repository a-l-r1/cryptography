import ec
import finite_field
from ec import EC, ECPoint
from finite_field import SM9G2

# y^2 = x^3 + b
t = 0x60000000_0058F98A
tr_t = 6 * (t ** 2) + 1
q_t = 36 * (t ** 4) + 36 * (t ** 3) + 24 * (t ** 2) + 6 * t + 1
p = q_t
a = 1
b = 0x05
n_t = 36 * (t ** 4) + 36 * (t ** 3) + 18 * (t ** 2) + 6 * t + 1
n = n_t
cf = 1
k = 12
# TODO: beta
# beta =
d_1 = 1
d_2 = 2
cid = 0x12

fp = finite_field.get_prime_finite_field_element_class(q_t, 'fp')
ec_g_1 = EC(fp(a), fp(b))
# TODO: correct?
ec_g_2 = EC(SM9G2(fp(a)), SM9G2(fp(b)))

x_p_1 = 0x93DE051D_62BF718F_F5ED0704_487D01D6_E1E40869_09DC3280_E8C4E481_7C66DDDD
y_p_1 = 0x21FE8DDA_4F21E607_63106512_5C395BBC_1C1C00CB_FA602435_0C464CD7_0A3EA616
p_1 = ECPoint(ec_g_1, fp(x_p_1), fp(y_p_1))

x_p_2 = (0x85AEF3D0_78640C98_597B6027_B441A01F_F1DD2C19_0F5E93C4_54806C11_D8806141,
         0x37227552_92130B08_D2AAB97F_D34EC120_EE265948_D19C17AB_F9B7213B_AF82D65B)
y_p_2 = (0x17509B09_2E845C12_66BA0D26_2CBEE6ED_0736A96F_A347C8BD_856DC76B_84EBEB96,
         0xA7CF28D5_19BE3DA6_5F317015_3D278FF2_47EFBA98_A71A0811_6215BBA5_C999A7C7)
p_2 = ECPoint(ec_g_2, SM9G2(fp(x_p_2[0]), fp(x_p_2[1])), SM9G2(fp(y_p_2[0]), fp(y_p_2[1])))

eid = 0x04

# don't know how to generate it
hid = bytes((0x42,))
