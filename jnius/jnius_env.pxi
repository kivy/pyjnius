
cdef JNIEnv *default_env = NULL

cdef extern int gettid()
cdef JavaVM *jvm = NULL

cdef JNIEnv *get_jnienv() except NULL:
    global default_env
    # first call, init.
    if default_env == NULL:
        default_env = get_platform_jnienv()
        if default_env == NULL:
            return NULL
        default_env[0].GetJavaVM(default_env, &jvm)

    # return the current env attached to the thread
    # XXX it threads are created from C (not java), we'll leak here.
    cdef JNIEnv *env = NULL
    jvm[0].AttachCurrentThread(jvm, &env, NULL)
    return env


def detach():
    jvm[0].DetachCurrentThread(jvm)

