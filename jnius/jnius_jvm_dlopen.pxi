include "config.pxi"
import os
from shlex import split
from subprocess import check_output, CalledProcessError
from os.path import dirname, join, exists
from os import readlink
from sys import platform
from .env import get_jnius_lib_location


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


cdef find_java_home():
    if platform in ('linux2', 'linux'):
        java = check_output(split('which javac')).strip()
        if not java:
            java = check_output(split('which java')).strip()
            if not java:
                return

        while True:
            try:
                java = readlink(java)
            except OSError:
                break
        return dirname(dirname(java)).decode('utf8')
    
    if platform == 'darwin':
        MAC_JAVA_HOME='/usr/libexec/java_home'
        # its a mac
        if not exists(MAC_JAVA_HOME):
            # I believe this always exists, but just in case
            return
        try:
            java = check_output(MAC_JAVA_HOME).strip().decode('utf8')
            return java
        except CalledProcessError as exc:
            # java_home return non-zero exit code if no Javas are installed
            return
        


cdef void create_jnienv() except *:
    cdef JavaVM* jvm
    cdef JavaVMInitArgs args
    cdef JavaVMOption *options
    cdef int ret
    cdef bytes py_bytes
    cdef void *handle
    import jnius_config

    JAVA_HOME = os.getenv('JAVA_HOME') or find_java_home()
    if JAVA_HOME is None or JAVA_HOME == '':
        raise SystemError("JAVA_HOME is not set, and unable to guess JAVA_HOME")
    cdef str JNIUS_LIB_SUFFIX = get_jnius_lib_location(JNIUS_PLATFORM)

    IF JNIUS_PYTHON3:
        try:
            jnius_lib_suffix = JNIUS_LIB_SUFFIX.decode("utf-8")
        except AttributeError:
            jnius_lib_suffix = JNIUS_LIB_SUFFIX
        lib_path = str_for_c(os.path.join(JAVA_HOME, jnius_lib_suffix))
    ELSE:
        lib_path = str_for_c(os.path.join(JAVA_HOME, JNIUS_LIB_SUFFIX))

    handle = dlopen(lib_path, RTLD_NOW | RTLD_GLOBAL)

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
    import traceback
    jnius_config.vm_started_at = ''.join(traceback.format_stack())

cdef JNIEnv *get_platform_jnienv() except NULL:
    if _platform_default_env == NULL:
        create_jnienv()
    return _platform_default_env
