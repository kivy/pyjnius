package org.jnius;

import java.util.logging.Logger;

/** Give caller-sensitive Logger factories a Java caller when invoked from JNI. */
public final class LoggerHelper {
    private LoggerHelper() {
    }

    public static Logger getLogger(String name) {
        return Logger.getLogger(name);
    }

    public static Logger getLogger(String name, String resourceBundleName) {
        return Logger.getLogger(name, resourceBundleName);
    }
}
