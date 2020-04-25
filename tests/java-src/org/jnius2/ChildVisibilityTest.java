package org.jnius2;

import java.lang.String;

import org.jnius.VisibilityTest;

public class ChildVisibilityTest extends VisibilityTest {
    public String fieldChildPublic = "ChildPublic";
    String fieldChildPackageProtected = "ChildPackageProtected";
    protected String fieldChildProtected = "ChildProtected";
    private String fieldChildPrivate = "ChildPrivate";

    static public String fieldChildStaticPublic = "ChildStaticPublic";
    static String fieldChildStaticPackageProtected = "ChildStaticPackageProtected";
    static protected String fieldChildStaticProtected = "ChildStaticProtected";
    static private String fieldChildStaticPrivate = "ChildStaticPrivate";

    public String methodChildPublic() {
        return fieldChildPublic;
    }

    String methodChildPackageProtected() {
        return fieldChildPackageProtected;
    }

    protected String methodChildProtected() {
        return fieldChildProtected;
    }

    private String methodChildPrivate() {
        return fieldChildPrivate;
    }

    protected boolean methodMultiArgs(boolean a, boolean b) {
        return a & !b;
    }

    private boolean methodMultiArgs(boolean a, boolean b, boolean c) {
        return a & !b & c;
    }

    // dummy method to avoid warning about unused methods
    public String methodChildDummy() {
        this.methodMultiArgs(true, true, false);
        return this.methodChildPrivate();
    }

    static public String methodChildStaticPublic() {
        return fieldChildStaticPublic;
    }

    static String methodChildStaticPackageProtected() {
        return fieldChildStaticPackageProtected;
    }

    static protected String methodChildStaticProtected() {
        return fieldChildStaticProtected;
    }

    static private String methodChildStaticPrivate() {
        return fieldChildStaticPrivate;
    }

    static protected boolean methodStaticMultiArgs(boolean a, boolean b) {
        return a & !b;
    }

    static private boolean methodStaticMultiArgs(boolean a, boolean b, boolean c) {
        return a & !b & c;
    }

    // dummy method to avoid warning about unused methods
    static public String methodChildStaticDummy() {
        ChildVisibilityTest.methodStaticMultiArgs(true, true, true);
        return ChildVisibilityTest.methodChildStaticPrivate();
    }
}
