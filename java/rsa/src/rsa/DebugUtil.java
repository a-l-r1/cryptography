package rsa;

class DebugUtil {
    private final static char[] hexArray = "0123456789abcdef ".toCharArray();

    static String bytesToHex(byte[] bytes) {
        char[] hexChars = new char[bytes.length * 3];
        for ( int j = 0; j < bytes.length; j++ ) {
            int v = bytes[j] & 0xFF;
            hexChars[j * 3] = hexArray[v >>> 4];
            hexChars[j * 3 + 1] = hexArray[v & 0x0F];
            hexChars[j * 3 + 2] = hexArray[16];
        }

        return new String(hexChars);
    }

    static void byteArrayDump(byte[] bytes) {
        System.out.println(bytesToHex(bytes));
    }
}
