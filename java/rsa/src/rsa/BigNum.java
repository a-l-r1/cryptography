package rsa;

import java.security.SecureRandom;
import java.util.Arrays;

public class BigNum {
    private static final int ARRAY_LENGTH = 128;
    private int[] data;
    private static final SecureRandom random = new SecureRandom();

    BigNum () {
        this.data = new int[ARRAY_LENGTH];
    }

    BigNum (int n) {
        this.data = new int[ARRAY_LENGTH];

        this.data[0] = n;
    }

    BigNum (long n) {
        int low = (int)(n & 0xffffffffL);
        int high = (int)((n & 0xffffffff00000000L) >> 32);

        this.data = new int[ARRAY_LENGTH];

        this.data[0] = low;
        this.data[1] = high;
    }

    BigNum (BigNum bn) {
        this.data = new int[ARRAY_LENGTH];
        System.arraycopy(bn.data, 0, this.data, 0, ARRAY_LENGTH);
    }

    BigNum (String str) throws IllegalArgumentException {
        this.data = new int[ARRAY_LENGTH];

        try {
            for (int i = 0; i < ARRAY_LENGTH; i++) {
                String currentChunk = str.substring(3 + 9 * i, 3 + 7 + 9 * i + 1);
                this.data[ARRAY_LENGTH - i - 1] = Integer.parseUnsignedInt(currentChunk, 16);
            }
        } catch (ArrayIndexOutOfBoundsException e) {
            throw new IllegalArgumentException("invalid dump string");
        }
    }

    BigNum (byte[] bytes) throws IllegalArgumentException {
        this.data = new int[ARRAY_LENGTH];

        int length = bytes.length;
        for (int i = 0; i < length; i++) {
            this.setByte(length - i - 1, bytes[i]);
        }
    }

    BigNum add(BigNum other) throws ArithmeticException {
        int carry = 0;
        long tmp;
        BigNum result = new BigNum();

        for (int i = 0; i < ARRAY_LENGTH; i++)
        {
            tmp = Integer.toUnsignedLong(this.data[i]) + Integer.toUnsignedLong(other.data[i]) + carry;
            result.data[i] = (int)(tmp);

            if (Long.compareUnsigned(tmp, 0xffffffffL) <= 0) {
                carry = 0;
            } else {
                carry = 1;
            }
        }

        if (carry == 1) {
            throw new ArithmeticException("overflow");
        }

        return result;
    }

    BigNum sub(BigNum other) throws ArithmeticException {
        int borrow = 0;
        long res;
        long tmp1;
        long tmp2;

        BigNum result = new BigNum();

        for (int i = 0; i < ARRAY_LENGTH; i++) {
            tmp1 = Integer.toUnsignedLong(this.data[i]) + 0x100000000L;
            tmp2 = Integer.toUnsignedLong(other.data[i]);
            res = tmp1 - borrow - tmp2;
            result.data[i] = (int)(res & 0xffffffffL);

            if (Long.compareUnsigned(res, 0xffffffffL) <= 0) {
                borrow = 1;
            } else {
                borrow = 0;
            }
        }

        if (borrow == 1) {
            throw new ArithmeticException("overflow, negative result inferred");
        }

        return result;
    }

    BigNum leftShiftOneBit() throws ArithmeticException {
        if ((this.data[ARRAY_LENGTH - 1] & 0x8000000000000000L) == 0x8000000000000000L) {
            throw new ArithmeticException("overflow, highest bit is 1");
        }

        BigNum result = new BigNum();

        int i;
        for (i = ARRAY_LENGTH - 1; i >= 1; i--) {
            result.data[i] = (this.data[i] << 1) | ((this.data[i - 1] >> 31) & 0x00000001);
        }
        result.data[0] = this.data[0] << 1;

        return result;
    }

    BigNum rightShiftOneBit() throws ArithmeticException {
        BigNum result = new BigNum();

        int i;
        for (i = 0; i < ARRAY_LENGTH - 1; i++) {
            result.data[i] = ((this.data[i] >> 1) & 0x7fffffff) | (this.data[i + 1] << 31);
        }
        result.data[ARRAY_LENGTH - 1] = this.data[ARRAY_LENGTH - 1] >> 1;

        return result;
    }

    BigNum or(BigNum other) {
        BigNum result = new BigNum();

        for (int i = 0; i < ARRAY_LENGTH; i++) {
            result.data[i] = this.data[i] | other.data[i];
        }

        return result;
    }

    BigNum and(BigNum other) {
        BigNum result = new BigNum();

        for (int i = 0; i < ARRAY_LENGTH; i++) {
            result.data[i] = this.data[i] & other.data[i];
        }

        return result;
    }

    BigNum xor(BigNum other) {
        BigNum result = new BigNum();

        for (int i = 0; i < ARRAY_LENGTH; i++) {
            result.data[i] = this.data[i] ^ other.data[i];
        }

        return result;
    }

    BigNum mul(BigNum other) throws ArithmeticException {
        BigNum result = new BigNum();
        long intermediate;
        int high, low;

        int thisChunkLength = this.getChunkLength();
        int otherChunkLength = other.getChunkLength();

        for (int i = 0; i < thisChunkLength; i++) {
            BigNum row = new BigNum();

            for (int j = 0; j < otherChunkLength; j++) {
                BigNum tmp = new BigNum();

                intermediate = Integer.toUnsignedLong(this.data[i]) * Integer.toUnsignedLong(other.data[j]);
                high = (int)((intermediate & 0xffffffff00000000L) >> 32);
                low = (int)(intermediate & 0xffffffffL);
                tmp.data[i + j] = low;
                try {
                    tmp.data[i + j + 1] = high;
                } catch (ArrayIndexOutOfBoundsException e) {
                    /* When i + j == ARRAY_LENGTH - 1, the exception will occur.
                       If the high part != 0, an overflow will occur.
                     */
                    if (high != 0) {
                        throw new ArithmeticException("overflow, result too large to store");
                    }
                }

                row = row.add(tmp);
            }

            result = result.add(row);
        }

        return result;
    }

    int compare(BigNum other) {
        for (int i = ARRAY_LENGTH - 1; i >= 0; i--) {
            if (Integer.compareUnsigned(this.data[i], other.data[i]) < 0) {
                return -1;
            }

            if (Integer.compareUnsigned(this.data[i], other.data[i]) > 0) {
                return 1;
            }
        }

        return 0;
    }

    /* {quotient, remainder} */
    BigNum[] divmod(BigNum other) {
        BigNum zero = new BigNum(0);

        BigNum dividend = new BigNum(this);
        BigNum denominator = new BigNum(other);
        BigNum current = new BigNum(1);

        BigNum quotient = new BigNum();

        final long half_max = 0x8000000000000000L;
        boolean overflow = false;

        while (this.compare(denominator) >= 0) {
            if (Long.compareUnsigned(denominator.data[ARRAY_LENGTH - 1], half_max) >= 0) {
                overflow = true;
                break;
            }

            current = current.leftShiftOneBit();
            denominator = denominator.leftShiftOneBit();
        }

        if (!overflow) {
            current = current.rightShiftOneBit();
            denominator = denominator.rightShiftOneBit();
        }

        while (current.compare(zero) != 0) {
            if (dividend.compare(denominator) >= 0) {
                dividend = dividend.sub(denominator);
                quotient = quotient.or(current);
            }

            current = current.rightShiftOneBit();
            denominator = denominator.rightShiftOneBit();
        }

        BigNum[] result = new BigNum[2];
        result[0] = quotient;
        result[1] = dividend;

        return result;
    }

    BigNum div(BigNum other) {
        return this.divmod(other)[0];
    }

    BigNum mod(BigNum other) {
        return this.sub(other.mul(this.div(other)));
    }

    boolean getBit(int index) throws IllegalArgumentException {
        if (index >= ARRAY_LENGTH * 32 || index < 0) {
            throw new IllegalArgumentException("out of range");
        }

        int bitmask = 1 << index % 32;
        int array_index = index / 32;

        return (this.data[array_index] & bitmask) == bitmask;
    }

    int getMSBIndex() {
        for (int i = ARRAY_LENGTH * 32 - 1; i >= 0; i--) {
            if (this.getBit(i)) {
                return i + 1;
            }
        }

        /* this is 0 */
        return 0;
    }

    BigNum modularPow(BigNum power, BigNum modulus) {
        BigNum result = new BigNum(1);
        int msbIndex = power.getMSBIndex();

        for (int i = msbIndex - 1; i >= 0; i--) {
            result = result.mul(result);
            result = result.mod(modulus);

            if (power.getBit(i)) {
                result = result.mul(this);
                result = result.mod(modulus); /* culprit when i == 0 */
            }
        }

        return result;
    }

    BigNum gcd(BigNum other) {
        BigNum a = new BigNum(this);
        BigNum b = new BigNum(other);
        BigNum tmp;

        BigNum zero = new BigNum(0);

        while (!(b.equals(zero))) {
            tmp = a.mod(b);
            a = b;
            b = tmp;
        }

        return a;
    }

    boolean isCoprimeWith(BigNum other) {
        return this.gcd(other).equals(new BigNum(1));
    }

    BigNum modularInverse(BigNum modulus) throws UnsupportedOperationException {
        if (!(this.isCoprimeWith(modulus))) {
            throw new UnsupportedOperationException("not coprime");
        }

        /* {r, q, x, y} */
        BigNum[] lastLastResult = new BigNum[4], lastResult = new BigNum[4], result = new BigNum[4];

        lastLastResult[0] = new BigNum(this);
        lastLastResult[1] = new BigNum(0);
        lastLastResult[2] = new BigNum(1);
        lastLastResult[3] = new BigNum(0);

        lastResult[0] = new BigNum(modulus);
        lastResult[1] = new BigNum(0);
        lastResult[2] = new BigNum(0);
        lastResult[3] = new BigNum(1);

        while (!lastResult[0].equals(new BigNum(0))) {
            result[0] = lastLastResult[0].mod(lastResult[0]);
            result[1] = lastLastResult[0].div(lastResult[0]);
            result[2] = lastLastResult[2].add(modulus).sub(result[1].mul(lastResult[2]).mod(modulus)).mod(modulus);
            result[3] = lastLastResult[3].add(modulus).sub(result[1].mul(lastResult[3]).mod(modulus)).mod(modulus);

            lastLastResult = lastResult;
            lastResult = result;
            result = new BigNum[4];
        }

        return lastLastResult[2].mod(modulus);
    }

    static BigNum CRT(BigNum[] a, BigNum[] n) throws UnsupportedOperationException {
        if (a.length != 2 || n.length != 2) {
            throw new UnsupportedOperationException("unsupported array length");
        }

        BigNum[] m = new BigNum[2];
        m[0] = n[0].modularInverse(n[1]);
        m[1] = n[1].modularInverse(n[0]);

        return a[0].mul(m[1]).mul(n[1]).add(a[1].mul(m[0]).mul(n[0])).mod(n[0].mul(n[1]));
    }

    String toString(int indexUpperBound) {
        String result = "";

        result += "0x";

        for (int i = indexUpperBound - 1; i >= 0; i--)
        {
            result += "_";
            result += String.format("%8s", Integer.toUnsignedString(this.data[i], 16)).replace(" ", "0");
        }

        return result;
    }

    @Override
    public String toString() {
        return this.toString(ARRAY_LENGTH);
    }

    void dump(int indexUpperBound) {
        System.out.println(this.toString(indexUpperBound));
    }

    void dump() {
        this.dump(ARRAY_LENGTH);
    }

    byte getByte(int index) throws IllegalArgumentException {
        if (index >= ARRAY_LENGTH * 4 || index < 0) {
            throw new IllegalArgumentException("out of range");
        }

        int curr_int = this.data[index / 4];
        int byte_index = index % 4;
        byte result = 0;

        switch (byte_index) {
            case 0:
                result = (byte)(curr_int & 0x000000ff);
                break;
            case 1:
                result = (byte)((curr_int & 0x0000ff00) >> 8);
                break;
            case 2:
                result = (byte)((curr_int & 0x00ff0000) >> 16);
                break;
            case 3:
                result = (byte)((curr_int & 0xff000000) >> 24);
                break;
        }

        return result;
    }

    void setByte(int index, byte b) throws IllegalArgumentException {
        if (index >= ARRAY_LENGTH * 4 || index < 0) {
            throw new IllegalArgumentException("out of range");
        }

        int byte_index = index % 4;

        switch (byte_index) {
            case 0:
                this.data[index / 4] &= 0xffffff00;
                this.data[index / 4] |= Byte.toUnsignedInt(b);
                break;
            case 1:
                this.data[index / 4] &= 0xffff00ff;
                this.data[index / 4] |= Byte.toUnsignedInt(b) << 8;
                break;
            case 2:
                this.data[index / 4] &= 0xff00ffff;
                this.data[index / 4] |= Byte.toUnsignedInt(b) << 16;
                break;
            case 3:
                this.data[index / 4] &= 0x00ffffff;
                this.data[index / 4] |= Byte.toUnsignedInt(b) << 24;
                break;
        }
    }

    int getByteLength() {
        for (int i = ARRAY_LENGTH * 4 - 1; i >= 0; i--) {
            if (this.getByte(i) != 0) {
                return i + 1;
            }
        }

        /* this is 0 */
        return 0;
    }

    byte[] toByteArray(int byteLength) throws IllegalArgumentException {
        if (byteLength == 0) {
            return new byte[1];
        }

        byte[] result = new byte[byteLength];

        for (int i = 0; i < byteLength; i++) {
            result[byteLength - i - 1] = this.getByte(i);
        }

        return result;
    }

    byte[] toByteArray() {
        return this.toByteArray(this.getByteLength());
    }

    int getChunkLength() {
        for (int i = ARRAY_LENGTH - 1; i >= 0; i--) {
            if (this.data[i] != 0) {
                return i + 1;
            }
        }

        /* this is 0 */
        return 0;
    }

    static BigNum randBelow(BigNum upperBound) throws IllegalArgumentException {
        int chunkLength = upperBound.getChunkLength();

        if (chunkLength == 0) {
            throw new IllegalArgumentException("upper bound is 0");
        }

        BigNum result = new BigNum();

        for (int i = chunkLength - 1; i >= 0; i--) {
            if (i == chunkLength - 1) {
                /* XXX: uneven probability? */
                result.data[i] = Integer.remainderUnsigned(random.nextInt(), upperBound.data[chunkLength - 1]);
            } else {
                result.data[i] = random.nextInt();
            }
        }

        return result;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == null) {
            return false;
        }

        if (obj == this) {
            return true;
        }

        if (!(obj instanceof BigNum)) {
            return false;
        }

        return Arrays.equals(((BigNum)obj).data, this.data);
    }
}
