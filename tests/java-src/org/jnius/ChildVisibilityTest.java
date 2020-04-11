package org.jnius;

import java.lang.String;

public class ChildVisibilityTest extends VisibilityTest {
    public String fieldChildPublic = "ChildPublic";
    protected String fieldChildProtected = "ChildProtected";
    private String fieldChildPrivate = "ChildPrivate";

    static public String fieldChildStaticPublic = "ChildStaticPublic";
    static protected String fieldChildStaticProtected = "ChildStaticProtected";
    static private String fieldChildStaticPrivate = "ChildStaticPrivate";

    public String methodChildPublic() {
        return fieldChildPublic;
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
