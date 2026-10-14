package org.jnius;

public class MethodBindingTest {
    private final String value;

    public MethodBindingTest(String value) {
        this.value = value;
    }

    public String single() {
        return value;
    }

    public String multiple() {
        return value;
    }

    public String multiple(String suffix) {
        return value + suffix;
    }

    public static String staticSingle() {
        return "static";
    }

    public static String staticMultiple() {
        return "static";
    }

    public static String staticMultiple(String suffix) {
        return "static" + suffix;
    }
}
