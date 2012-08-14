# on desktop, we need to create an env :)
# example taken from http://www.inonit.com/cygwin/jni/invocationApi/c.html

cdef extern jint JNI_CreateJavaVM(JavaVM **pvm, void **penv, void *args)
cdef extern from "jni.h":
    int JNI_VERSION_1_4
    jboolean JNI_FALSE
    ctypedef struct JavaVMInitArgs:
        jint version
        jint nOptions
        jboolean ignoreUnrecognized

cdef JNIEnv *default_env = NULL

cdef void create_jnienv():
    cdef JavaVM* jvm
    cdef JavaVMInitArgs args

    args.version = JNI_VERSION_1_4
    args.nOptions = 0
    args.ignoreUnrecognized = JNI_FALSE

    JNI_CreateJavaVM(&jvm, <void **>&default_env, &args)

cdef JNIEnv *get_jnienv():
    if default_env == NULL:
        create_jnienv()
    return default_env
