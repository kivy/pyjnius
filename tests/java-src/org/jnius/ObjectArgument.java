package org.jnius;


public class ObjectArgument {
    public static int checkObject(Object obj) {
        if (obj == null) {
            return -1;
        } else {
            return 0;
        }
    }
}
