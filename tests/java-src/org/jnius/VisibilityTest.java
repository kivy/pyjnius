package org.jnius;

import java.lang.String;

public class VisibilityTest {
    public String fieldPublic = "fieldPublic";
    protected String fieldProtected = "fieldProtected";
    private String fieldPrivate = "fieldPrivate";

    static public String fieldStaticPublic = "fieldStaticPublic";
    static protected String fieldStaticProtected = "fieldStaticProtected";
    static private String fieldStaticPrivate = "fieldStaticPrivate";

    public String methodPublic() {
        return "methodPublic";
    }

    protected String methodProtected() {
        return "methodProtected";
    }

    private String methodPrivate() {
        return "methodPrivate";
    }

    static public String methodStaticPublic() {
        return "methodStaticPublic";
    }

    static protected String methodStaticProtected() {
        return "methodStaticProtected";
    }

    static private String methodStaticPrivate() {
        return "methodStaticPrivate";
    }
}