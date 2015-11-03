from cpython.version cimport PY_MAJOR_VERSION

# on desktop, we need to create an env :)
# example taken from http://www.inonit.com/cygwin/jni/invocationApi/c.html

cdef extern jint __stdcall JNI_CreateJavaVM(JavaVM **pvm, void **penv, void *args)
cdef extern from "jni.h":
    int JNI_VERSION_1_4
    int JNI_OK
    jboolean JNI_FALSE
    ctypedef struct JavaVMInitArgs:
        jint version
        jint nOptions
        jboolean ignoreUnrecognized
        JavaVMOption *options
    ctypedef struct JavaVMOption:
        char *optionString
        void *extraInfo

cdef JNIEnv *_platform_default_env = NULL

cdef void create_jnienv() except *:
    cdef JavaVM* jvm
    cdef JavaVMInitArgs args
    cdef JavaVMOption *options
    cdef int ret
    cdef bytes py_bytes
    import jnius_config

    optarr = jnius_config.options
    optarr.append("-Djava.class.path=" + jnius_config.expand_classpath())

    options = <JavaVMOption*>malloc(sizeof(JavaVMOption) * len(optarr))
    for i, opt in enumerate(optarr):
        if PY_MAJOR_VERSION >= 3:
           opt = opt.encode('utf-8')
        options[i].optionString = <bytes>(opt)
        options[i].extraInfo = NULL

    args.version = JNI_VERSION_1_4
    args.options = options
    args.nOptions = len(optarr)
    args.ignoreUnrecognized = JNI_FALSE

    ret = JNI_CreateJavaVM(&jvm, <void **>&_platform_default_env, &args)
    free(options)

    if ret != JNI_OK:
        raise SystemError("JVM failed to start")

    jnius_config.vm_running = True

cdef JNIEnv *get_platform_jnienv() except NULL:
    if _platform_default_env == NULL:
        create_jnienv()
    return _platform_default_env
