import sys
import os
from os.path import join
from jnius.env import get_jdk_home
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
    cp = jnius_config.expand_classpath()
    optarr.append("-Djava.class.path={0}".format(cp))

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

    if sys.version_info >= (3, 8):
        # uh, let's see if this works and cleanup later
        jdk_home = get_jdk_home('win32')
        for suffix in (
            ('bin', 'client'),
            ('bin', 'server'),
            ('jre', 'bin', 'client'),
            ('jre', 'bin', 'server'),
        ):
            path = join(jdk_home, *suffix)
            if not os.path.isdir(path):
                continue
            with os.add_dll_directory(path):
                try:
                    ret = JNI_CreateJavaVM(&jvm, <void **>&_platform_default_env, &args)
                except Exception as e:
                    pass
                else:
                    break
        else:
            raise Exception("Unable to create jni env, no jvm dll found.")

    else:
        ret = JNI_CreateJavaVM(&jvm, <void **>&_platform_default_env, &args)

    free(options)

    if ret != JNI_OK:
        raise SystemError("JVM failed to start")

    jnius_config.vm_running = True

cdef JNIEnv *get_platform_jnienv() except NULL:
    if _platform_default_env == NULL:
        create_jnienv()
    return _platform_default_env
