# on desktop, we need to create an env :)
# example taken from http://www.inonit.com/cygwin/jni/invocationApi/c.html

cdef extern jint __stdcall JNI_CreateJavaVM(JavaVM **pvm, void **penv, void *args)
cdef extern from "jni.h":
    int JNI_VERSION_1_4
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

def classpath():
    import platform
    from glob import glob
    from os import environ
    from os.path import realpath, dirname, join

    if platform.system() == 'Windows':
        split_char = ';'
    else:
        split_char = ':'

    paths = [realpath('.'), join(dirname(__file__), 'src'), ]
    if 'CLASSPATH' not in environ:
        return split_char.join(paths)

    cp = environ.get('CLASSPATH')
    pre_paths = paths + cp.split(split_char)
    # deal with wildcards
    for path in pre_paths:
        if not path.endswith('*'):
            paths.append(path)
        else:
            paths.extend(glob(path + '.jar'))
            paths.extend(glob(path + '.JAR'))
    result = split_char.join(paths)
    return result


cdef void create_jnienv():
    cdef JavaVM* jvm
    cdef JavaVMInitArgs args
    cdef JavaVMOption options[1]
    cdef bytes py_bytes

    cp = classpath()
    py_bytes = <bytes>('-Djava.class.path={0}'.format(cp).encode())
    options[0].optionString = py_bytes
    options[0].extraInfo = NULL 

    args.version = JNI_VERSION_1_4
    args.options = options
    args.nOptions = 1
    args.ignoreUnrecognized = JNI_FALSE

    retorno = JNI_CreateJavaVM(&jvm, <void **>&_platform_default_env, &args)
    print("Creado")
    print(retorno)

cdef JNIEnv *get_platform_jnienv():
    if _platform_default_env == NULL:
        create_jnienv()
    return _platform_default_env
