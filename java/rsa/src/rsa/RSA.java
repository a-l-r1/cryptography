package rsa;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;

import static rsa.BigNum.CRT;

class RSA {
    private static final BigNum e = new BigNum(65537);

    static BigNum genPrime(int bitLength) {
        BigNum upperBound = new BigNum(1);
        for (int i = 0; i < bitLength - 1; i++) {
            upperBound = upperBound.leftShiftOneBit();
        }

        BigNum result;
        int iterationCount = 10;
        int generationCount = 0;

        do {
            generationCount++;
            System.out.println("genPrime: generation " + generationCount);
            result = BigNum.randBelow(upperBound);
        } while (!BigNumPrimalityTest.primalityTest(result, iterationCount));

        return result;
    }

    /* {{d, n, p, q}, {e, n}} */
    static BigNum[][] genKeyPair(BigNum p, BigNum q) {
        BigNum one = new BigNum(1);

        BigNum n = p.mul(q);
        BigNum phi_n = p.sub(one).mul(q.sub(one));

        BigNum d = e.modularInverse(phi_n);

        BigNum[] sk = new BigNum[4];
        sk[0] = d;
        sk[1] = n;
        sk[2] = p;
        sk[3] = q;

        BigNum[] pk = new BigNum[2];
        pk[0] = e;
        pk[1] = n;

        BigNum[][] result = new BigNum[2][];
        result[0] = sk;
        result[1] = pk;

        return result;
    }

    static BigNum[][] genKeyPair(int bitLength) {
        System.out.println("genKeyPair: generating p");
        BigNum p = genPrime(bitLength);
        System.out.println("genKeyPair: generating q");
        BigNum q = genPrime(bitLength);

        return genKeyPair(p, q);
    }

    static BigNum encrypt(BigNum plainText, BigNum[] publicKey) throws IllegalArgumentException{
        if (plainText.compare(publicKey[1]) != -1) {
            throw new IllegalArgumentException("plaintext chunk larger than n");
        }

        return plainText.modularPow(publicKey[0], publicKey[1]);
    }

    static BigNum decryptClassic(BigNum cipherText, BigNum[] privateKey) throws IllegalArgumentException {
        if (cipherText.compare(privateKey[1]) != -1) {
            throw new IllegalArgumentException("ciphertext chunk larger than n");
        }

        return cipherText.modularPow(privateKey[0], privateKey[1]);
    }

    static BigNum decrypt(BigNum ciphertext, BigNum[] privateKey) throws IllegalArgumentException {
        BigNum d = privateKey[0];
        BigNum n = privateKey[1];
        BigNum p = privateKey[2];
        BigNum q = privateKey[3];

        BigNum x = ciphertext.modularPow(d, n);

        BigNum[] aArray = new BigNum[2];
        aArray[0] = x;
        aArray[1] = x;
        BigNum[] nArray = new BigNum[2];
        nArray[0] = p;
        nArray[1] = q;

        return CRT(aArray, nArray);
    }

    static byte[] hexStringToByteArray(String s) {
        int len = s.length();
        byte[] data = new byte[len / 2];

        for (int i = 0; i < len; i += 2) {
            data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
                    + Character.digit(s.charAt(i+1), 16));
        }

        return data;
    }

    private static byte[] mgf(byte[] mgfSeed, int maskLen) {
        byte[] t = new byte[0];

        /* SHA-256 */
        int hLen = 32;

        int counter;
        byte[] c = new byte[4];
        int counterUpperBound;
        if (maskLen % hLen == 0) {
            counterUpperBound = maskLen / hLen - 1;
        } else {
            counterUpperBound = maskLen / hLen;
        }

        for (counter = 0; counter <= counterUpperBound; counter++) {
            /* I2OSP is big endian */
            c[0] = (byte)((counter & 0xff000000) >> 24);
            c[1] = (byte)((counter & 0x00ff0000) >> 16);
            c[2] = (byte)((counter & 0x0000ff00) >> 8);
            c[3] = (byte)((counter & 0x000000ff));

            t = byteArrayConcat(t, getByteArraySHA256Hash(byteArrayConcat(mgfSeed, c)));
        }

        byte[] result = new byte[maskLen];
        int j;
        System.arraycopy(result, 0, t, 0, maskLen);

        return result;
    }

    private static byte[] byteArrayXor(byte[] a, byte[] b) throws IllegalArgumentException {
        if (a.length != b.length) {
            throw new IllegalArgumentException("two array not of equal length");
        }

        int length = a.length;
        byte[] result = new byte[length];

        for (int i = 0; i < length; i++) {
            result[i] = (byte)((a[i] ^ b[i]) & 0xff);
        }

        return result;
    }

    private static byte[] byteArrayConcat(byte[] ... args) {
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();

        try {
            for (byte[] arg : args) {
                outputStream.write(arg);
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }

        return outputStream.toByteArray();
    }

    static byte[] encryptOAEP(byte[] plainText, BigNum[] publicKey, String l) throws IllegalArgumentException {
        BigNum n = publicKey[1];
        int mLen = plainText.length;
        int k = n.getByteLength();

        /* SHA-256 */
        int hLen = 32;

        if (mLen > k - 2 * hLen - 2) {
            throw new IllegalArgumentException("message too long");
        }

        byte[] lHash = getStringSHA256Hash(l);

        int psLength = k - mLen - 2 * hLen - 2;
        byte[] ps = new byte[psLength];

        byte[] padding = new byte[1];
        padding[0] = 0x01;

        byte[] db = byteArrayConcat(lHash, ps, padding, plainText);

        SecureRandom random = new SecureRandom();
        byte[] seed = new byte[hLen];
        random.nextBytes(seed);

        byte[] dbMask = mgf(seed, k - hLen - 1);

        byte[] maskedDB = byteArrayXor(db, dbMask);

        byte[] seedMask = mgf(maskedDB, hLen);

        byte[] maskedSeed = byteArrayXor(seed, seedMask);

        byte[] padding1 = new byte[1];

        byte[] em = byteArrayConcat(padding1, maskedSeed, maskedDB);

        BigNum m = new BigNum(em);

        BigNum c = encrypt(m, publicKey);

        return c.toByteArray(k);
    }

    private static byte[] byteArraySlice(byte[] bytes, int start, int end) throws IllegalArgumentException {
        if (start > end || start < 0 || start >= bytes.length || end > bytes.length) {
            throw new IllegalArgumentException("invalid slice");
        }

        byte[] result = new byte[end - start];
        System.arraycopy(bytes, start, result, 0, end - start);
        return result;
    }

    static byte[] decryptOAEP(byte[] cipherText, BigNum[] privateKey, String l) throws IllegalArgumentException {
        BigNum n = privateKey[1];
        int k = n.getByteLength();

        /* SHA-256 */
        int hLen = 32;

        if (cipherText.length != k) {
            throw new IllegalArgumentException("ciphertext length != k");
        }

        if (k < 2 * hLen + 2) {
            throw new IllegalArgumentException("k < 2 * hLen + 2");
        }

        BigNum c = new BigNum(cipherText);

        BigNum m = RSA.decrypt(c, privateKey);

        byte[] em = m.toByteArray(k);

        byte[] lHash = getStringSHA256Hash(l);

        byte[] y = byteArraySlice(em, 0, 1);
        byte[] maskedSeed = byteArraySlice(em, 1, 1 + hLen);
        byte[] maskedDB = byteArraySlice(em, 1 + hLen, k);

        if (y[0] != 0) {
            throw new IllegalArgumentException("y is not 0");
        }

        byte[] seedMask = mgf(maskedDB, hLen);

        byte[] seed = byteArrayXor(maskedSeed, seedMask);

        byte[] dbMask = mgf(seed, k - hLen - 1);

        byte[] db = byteArrayXor(maskedDB, dbMask);

        byte[] lHash1 = byteArraySlice(db, 0, hLen);
        if (!Arrays.equals(lHash1, lHash)) {
            throw new IllegalArgumentException("hash not equal");
        }
        int mIndex = hLen;
        while (mIndex < db.length && db[mIndex] != 0x01) {
            mIndex++;
        }
        mIndex++;
        if (mIndex >= k) {
            throw new IllegalArgumentException("cannot find M");
        }

        return byteArraySlice(db, mIndex, db.length);
    }

    private static byte[] getStringSHA256Hash(String l) {
        MessageDigest md = null;
        try {
            md = MessageDigest.getInstance("SHA-256");
            md.reset();
            md.update(l.getBytes(StandardCharsets.UTF_8));
        } catch (NoSuchAlgorithmException ex) {
            ex.printStackTrace();
        }
        return Objects.requireNonNull(md).digest();
    }

    private static byte[] getByteArraySHA256Hash(byte[] b) {
        MessageDigest md = null;
        try {
            md = MessageDigest.getInstance("SHA-256");
            md.reset();
            md.update(b);
        } catch (NoSuchAlgorithmException ex) {
            ex.printStackTrace();
        }
        return Objects.requireNonNull(md).digest();
    }

    static void writeKey(Path path, BigNum[] key) throws IOException {
        String[] keyStrings = new String[key.length];

        for (int i = 0; i < key.length; i++) {
            keyStrings[i] = key[i].toString();
        }

        Files.write(path, Arrays.asList(keyStrings));
    }

    static void writePrivateKey(Path path, BigNum[] privateKey) throws IOException {
        writeKey(path, privateKey);
    }

    static void writePublicKey(Path path, BigNum[] publicKey) throws IOException {
        writeKey(path, publicKey);
    }

    static BigNum[] readKey(Path path) throws IOException {
        List<String> keyStringList = Files.readAllLines(path);

        Object[] keyStringArray = keyStringList.toArray();
        BigNum[] result = new BigNum[keyStringArray.length];
        for (int i = 0; i < keyStringArray.length; i++) {
            result[i] = new BigNum((String)keyStringArray[i]);
        }

        return result;
    }

    static BigNum[] readPrivateKey(Path path) throws IOException {
        return readKey(path);
    }

    static BigNum[] readPublicKey(Path path) throws IOException {
        return readKey(path);
    }

    static void encryptFile(Path plainTextPath, Path cipherTextPath, BigNum[] publicKey) {
        BigNum n = publicKey[1];
        int writeChunkByteLength = n.getByteLength();
        int readChunkByteLength = writeChunkByteLength - 1;

        byte[] plainTextCurrChunk = new byte[readChunkByteLength];

        try {
            FileInputStream plainTextInputStream = new FileInputStream(plainTextPath.toString());
            FileOutputStream cipherTextOutputStream = new FileOutputStream(cipherTextPath.toString());

            while (true) {
                int bytesRead = plainTextInputStream.read(plainTextCurrChunk);

                if (bytesRead == -1) {
                    break;
                }

                if (bytesRead == readChunkByteLength) {
                    BigNum m = new BigNum(plainTextCurrChunk);
                    byte[] c = RSA.encrypt(m, publicKey).toByteArray(writeChunkByteLength);

                    cipherTextOutputStream.write(c);
                } else {
                    for (int i = bytesRead; i < readChunkByteLength; i++) {
                        plainTextCurrChunk[i] = 0;
                    }
                    BigNum m = new BigNum(plainTextCurrChunk);
                    BigNum c = RSA.encrypt(m, publicKey);
                    byte[] cBytes = c.toByteArray(writeChunkByteLength);

                    cipherTextOutputStream.write(cBytes);
                }
            }

            plainTextInputStream.close();
            cipherTextOutputStream.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    static void decryptFile(Path plainTextPath, Path cipherTextPath, BigNum[] privateKey) {
        BigNum n = privateKey[1];
        int readChunkByteLength = n.getByteLength();
        int writeChunkByteLength = readChunkByteLength - 1;

        byte[] cipherTextCurrChunk = new byte[readChunkByteLength];

        try {
            FileInputStream cipherTextInputStream = new FileInputStream(cipherTextPath.toString());
            FileOutputStream plainTextOutputStream = new FileOutputStream(plainTextPath.toString());

            while (true) {
                int bytesRead = cipherTextInputStream.read(cipherTextCurrChunk);

                if (bytesRead == -1) {
                    break;
                }

                if (bytesRead == readChunkByteLength) {
                    BigNum m = new BigNum(cipherTextCurrChunk);
                    byte[] c = RSA.decrypt(m, privateKey).toByteArray(writeChunkByteLength);

                    plainTextOutputStream.write(c);
                } else {
                    BigNum m = new BigNum(cipherTextCurrChunk);
                    byte[] c = RSA.decrypt(m, privateKey).toByteArray(writeChunkByteLength);

                    plainTextOutputStream.write(c);
                }
            }

            cipherTextInputStream.close();
            plainTextOutputStream.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    static void encryptFileOAEP(Path plainTextPath, Path cipherTextPath, BigNum[] publicKey, String l) throws IOException {
        BigNum n = publicKey[1];
        int readChunkByteLength = 64;

        byte[] plainTextCurrChunk = new byte[readChunkByteLength];

        try {
            FileInputStream plainTextInputStream = new FileInputStream(plainTextPath.toString());
            FileOutputStream cipherTextOutputStream = new FileOutputStream(cipherTextPath.toString());

            while (true) {
                int bytesRead = plainTextInputStream.read(plainTextCurrChunk);

                if (bytesRead == -1) {
                    break;
                }

                if (bytesRead == readChunkByteLength) {
                    cipherTextOutputStream.write(encryptOAEP(plainTextCurrChunk, publicKey, l));
                } else {
                    for (int i = bytesRead; i < readChunkByteLength; i++) {
                        plainTextCurrChunk[i] = 0;
                    }
                    cipherTextOutputStream.write(encryptOAEP(plainTextCurrChunk, publicKey, l));
                }
            }

            plainTextInputStream.close();
            cipherTextOutputStream.close();
        } catch (IllegalArgumentException e) {
            e.printStackTrace();
        }
    }

    static void decryptFileOAEP(Path plainTextPath, Path cipherTextPath, BigNum[] privateKey, String l) throws IOException {
        BigNum n = privateKey[1];
        int readChunkByteLength = n.getByteLength();

        byte[] cipherTextCurrChunk = new byte[readChunkByteLength];

        try {
            FileInputStream cipherTextInputStream = new FileInputStream(cipherTextPath.toString());
            FileOutputStream plainTextOutputStream = new FileOutputStream(plainTextPath.toString());

            while (true) {
                int bytesRead = cipherTextInputStream.read(cipherTextCurrChunk);

                if (bytesRead == -1) {
                    break;
                }

                if (bytesRead == readChunkByteLength) {
                    plainTextOutputStream.write(decryptOAEP(cipherTextCurrChunk, privateKey, l));
                } else {
                    plainTextOutputStream.write(decryptOAEP(cipherTextCurrChunk, privateKey, l));
                }
            }

            cipherTextInputStream.close();
            plainTextOutputStream.close();
        } catch (IllegalArgumentException e) {
            e.printStackTrace();
        }
    }

    static void encryptFile(Path plainTextPath, Path cipherTextPath, Path publicKeyPath) throws IOException {
        encryptFile(plainTextPath, cipherTextPath, readPublicKey(publicKeyPath));
    }

    static void decryptFile(Path plainTextPath, Path cipherTextPath, Path privateKeyPath) throws IOException {
        decryptFile(plainTextPath, cipherTextPath, readPrivateKey(privateKeyPath));
    }

    static void encryptFileOAEP(Path plainTextPath, Path cipherTextPath, Path publicKeyPath, String l) throws IOException {
        encryptFileOAEP(plainTextPath, cipherTextPath, readPublicKey(publicKeyPath), l);
    }

    static void decryptFileOAEP(Path plainTextPath, Path cipherTextPath, Path privateKeyPath, String l) throws IOException {
        decryptFileOAEP(plainTextPath, cipherTextPath, readPrivateKey(privateKeyPath), l);
    }
}
