include "config.pxi"
import os

cdef extern from 'dlfcn.h' nogil:
    void* dlopen(const char *filename, int flag)
    char *dlerror()
    void *dlsym(void *handle, const char *symbol)
    int dlclose(void *handle)

    unsigned int RTLD_LAZY
    unsigned int RTLD_NOW
    unsigned int RTLD_GLOBAL
    unsigned int RTLD_LOCAL
    unsigned int RTLD_NODELETE
    unsigned int RTLD_NOLOAD
    unsigned int RTLD_DEEPBIND

    unsigned int RTLD_DEFAULT
    long unsigned int RTLD_NEXT


cdef extern from "jni.h":
    int JNI_VERSION_1_6
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

    JAVA_HOME = os.environ['JAVA_HOME']
    if JAVA_HOME is None or JAVA_HOME == '':
        raise SystemError("JAVA_HOME is not set.")
    IF JNIUS_PYTHON3:
        try:
            jnius_lib_suffix = JNIUS_LIB_SUFFIX.decode("utf-8")
        except AttributeError:
            jnius_lib_suffix = JNIUS_LIB_SUFFIX
        lib_path = str_for_c(os.path.join(JAVA_HOME, jnius_lib_suffix))
    ELSE:
        lib_path = str_for_c(os.path.join(JAVA_HOME, JNIUS_LIB_SUFFIX))

    cdef void *handle = dlopen(lib_path, RTLD_NOW | RTLD_GLOBAL)
    if handle == NULL:
        raise SystemError("Error calling dlopen({0}: {1}".format(lib_path, dlerror()))

    cdef void *jniCreateJVM = dlsym(handle, b"JNI_CreateJavaVM")

    if jniCreateJVM == NULL:
       raise SystemError("Error calling dlfcn for JNI_CreateJavaVM: {0}".format(dlerror()))

    optarr = jnius_config.options
    optarr.append("-Djava.class.path=" + jnius_config.expand_classpath())

    options = <JavaVMOption*>malloc(sizeof(JavaVMOption) * len(optarr))
    for i, opt in enumerate(optarr):
        optbytes = str_for_c(opt)
        options[i].optionString = <bytes>(optbytes)
        options[i].extraInfo = NULL

    args.version = JNI_VERSION_1_6
    args.options = options
    args.nOptions = len(optarr)
    args.ignoreUnrecognized = JNI_FALSE

    ret = (<jint (*)(JavaVM **pvm, void **penv, void *args)> jniCreateJVM)(&jvm, <void **>&_platform_default_env, &args)
    free(options)

    if ret != JNI_OK:
        raise SystemError("JVM failed to start: {0}".format(ret))

    jnius_config.vm_running = True

cdef JNIEnv *get_platform_jnienv() except NULL:
    if _platform_default_env == NULL:
        create_jnienv()
    return _platform_default_env
