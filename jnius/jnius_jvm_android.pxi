# on android, rely on SDL to get the JNI env
cdef extern JNIEnv *SDL_AndroidGetJNIEnv()


cdef JNIEnv *get_platform_jnienv() except NULL:
    return <JNIEnv*>SDL_AndroidGetJNIEnv()
