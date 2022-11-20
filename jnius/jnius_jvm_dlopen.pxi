include "config.pxi"
import os
from shlex import split
from subprocess import check_output, CalledProcessError
from os.path import dirname, join, exists
from os import readlink
from sys import platform
from .env import get_java_setup


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
    cdef void *handle
    import jnius_config

    JAVA_LOCATION = get_java_setup()
    cdef str java_lib = JAVA_LOCATION.get_jnius_lib_location()

    lib_path = str_for_c(java_lib)

    handle = dlopen(lib_path, RTLD_NOW | RTLD_GLOBAL)

    if handle == NULL:
        raise SystemError("Error calling dlopen({0}): {1}".format(lib_path, dlerror()))

    cdef void *jniCreateJVM = dlsym(handle, b"JNI_CreateJavaVM")

    if jniCreateJVM == NULL:
       raise SystemError("Error calling dlfcn for JNI_CreateJavaVM: {0}".format(dlerror()))

    optarr = jnius_config.options
    optarr.append("-Djava.class.path=" + jnius_config.expand_classpath())

    optarr = [str_for_c(x) for x in optarr]
    options = <JavaVMOption*>malloc(sizeof(JavaVMOption) * len(optarr))
    for i, opt in enumerate(optarr):
        options[i].optionString = <bytes>(opt)
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
    import traceback
    jnius_config.vm_started_at = ''.join(traceback.format_stack())

cdef JNIEnv *get_platform_jnienv() except NULL:
    if _platform_default_env == NULL:
        create_jnienv()
    return _platform_default_env
