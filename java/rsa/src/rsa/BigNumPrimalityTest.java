package rsa;

class BigNumPrimalityTest {
    static boolean primalityTest(BigNum bn, int iterations) {
        return fermat(bn, iterations);
    }

    static boolean millerRabin(BigNum bn, int iterations) {
        BigNum zero = new BigNum(0);
        BigNum one = new BigNum(1);
        BigNum two = new BigNum(2);
        BigNum three = new BigNum(3);

        if (bn.equals(one)) {
            return false;
        }

        if (bn.equals(two) || bn.equals(three)) {
            return true;
        }

        if (bn.mod(two).equals(zero)) {
            return false;
        }

        BigNum q = bn.sub(one);
        BigNum k = zero;

        while (q.mod(two).equals(zero)) {
            q = q.div(two);
            k = k.add(one);
        }

        for (int i = 0; i < iterations; i++) {
            boolean currPassResult = false;

            BigNum a = BigNum.randBelow(bn.sub(three));
            a = a.add(two);

            if (a.modularPow(q, bn).equals(one)) {
                continue;
            }

            BigNum currExponent = new BigNum();

            for (int j = 0; (new BigNum(j).compare(k) == -1); j++) {
                if (j == 0) {
                    currExponent = new BigNum(q);
                } else {
                    currExponent = currExponent.mul(two);
                }

                if (a.modularPow(currExponent, bn).equals(bn.sub(one))) {
                    currPassResult = true;
                    break;
                }
            }


            if (!currPassResult) {
                return false;
            }
        }

        return true;
    }

    static boolean fermat(BigNum bn, int iterations) {
        BigNum zero = new BigNum(0);
        BigNum one = new BigNum(1);
        BigNum two = new BigNum(2);
        BigNum three = new BigNum(3);

        if (bn.equals(one)) {
            return false;
        }

        if (bn.equals(two) || bn.equals(three)) {
            return true;
        }

        if (bn.mod(two).equals(zero)) {
            return false;
        }

        for (int i = 0; i < iterations; i++) {
            BigNum b = BigNum.randBelow(bn.sub(one));
            b = b.add(one);

            BigNum d = b.gcd(bn);

            if (d.compare(one) > 0) {
                return false;
            }

            if (b.modularPow(bn.sub(one), bn).compare(one) != 0) {
                return false;
            }
        }

        return true;
    }
}
