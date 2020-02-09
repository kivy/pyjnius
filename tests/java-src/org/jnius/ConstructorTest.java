package org.jnius;
import java.lang.Character;


public class ConstructorTest {
    public int ret;

    public ConstructorTest() {
        ret = 753;
    }

    public ConstructorTest(int cret) {
        ret = cret;
    }

    public ConstructorTest(char charet) {
        ret = (int) charet;
    }

    public ConstructorTest(int cret, char charet) {
        ret = cret + (int) charet;
    }

    public ConstructorTest(Object DO_NOT_CALL) {
        throw new Error();
    }

    public ConstructorTest(java.io.OutputStream os) {
        ret = 42;
    }
}
