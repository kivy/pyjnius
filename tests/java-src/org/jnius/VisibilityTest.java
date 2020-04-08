package org.jnius;

import java.lang.String;

public class VisibilityTest {
    public String fieldPublic = "Public";
    protected String fieldProtected = "Protected";
    private String fieldPrivate = "Private";

    static public String fieldStaticPublic = "StaticPublic";
    static protected String fieldStaticProtected = "StaticProtected";
    static private String fieldStaticPrivate = "StaticPrivate";

    public String methodPublic() {
        return fieldPublic;
    }

    protected String methodProtected() {
        return fieldProtected;
    }

    private String methodPrivate() {
        return fieldPrivate;
    }

    static public String methodStaticPublic() {
        return fieldStaticPublic;
    }

    static protected String methodStaticProtected() {
        return fieldStaticProtected;
    }

    static private String methodStaticPrivate() {
        return fieldStaticPrivate;
    }
}