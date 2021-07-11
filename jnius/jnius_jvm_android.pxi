# on android, rely on SDL to get the JNI env
cdef extern JNIEnv *SDL_ANDROID_GetJNIEnv()

cdef JNIEnv *get_platform_jnienv() except NULL:
    return SDL_ANDROID_GetJNIEnv()
