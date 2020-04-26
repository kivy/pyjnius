package org.jnius;

import java.lang.String;

public class VisibilityTest {
    public String fieldPublic = "Public";
    String fieldPackageProtected = "PackageProtected";
    protected String fieldProtected = "Protected";
    private String fieldPrivate = "Private";

    static public String fieldStaticPublic = "StaticPublic";
    static String fieldStaticPackageProtected = "StaticPackageProtected";
    static protected String fieldStaticProtected = "StaticProtected";
    static private String fieldStaticPrivate = "StaticPrivate";

    public String methodPublic() {
        return fieldPublic;
    }

    String methodPackageProtected() {
        return fieldPackageProtected;
    }

    protected String methodProtected() {
        return fieldProtected;
    }

    private String methodPrivate() {
        return fieldPrivate;
    }

    public boolean methodMultiArgs(boolean a) {
        return a;
    }

    // dummy method to avoid warning methodPrivate() isn't used
    public String methodDummy() {
        return this.methodPrivate();
    }

    static public String methodStaticPublic() {
        return fieldStaticPublic;
    }

    static String methodStaticPackageProtected() {
        return fieldStaticPackageProtected;
    }

    static protected String methodStaticProtected() {
        return fieldStaticProtected;
    }

    static private String methodStaticPrivate() {
        return fieldStaticPrivate;
    }

    static public boolean methodStaticMultiArgs(boolean a) {
        return a;
    }

    // dummy method to avoid warning methodStaticPrivate() isn't used
    static public String methodStaticDummy() {
        return VisibilityTest.methodStaticPrivate();
    }
}
