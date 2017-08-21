package org.jnius;

public class MultipleMethods {

    public static String resolve() {
	return "resolved no args";
    }

    public static String resolve(String i) {
	return "resolved one arg";
    }

    public static String resolve(String i, String j) {
	return "resolved two args";
    }

    public static String resolve(String i, String j, int k) {
	return "resolved two string and an integer";
    }

    public static String resolve(String i, String j, int k, int l) {
	return "resolved two string and two integers";
    }

    public static String resolve(String i, String j, int... integers) {
	return "resolved two args and varargs";
    }

    public static String resolve(int... integers) {
	return "resolved varargs";
    }

    public static String resolve(int i, long j, String k) {
    return "resolved one int, one long and a string";
    }
}
