package org.jnius;

import java.io.Closeable;

public class CloseableClass implements Closeable{
    public static boolean open = true;

    public CloseableClass() {
        open = true;
    }

    public void close() {
        open = false;
    }
}