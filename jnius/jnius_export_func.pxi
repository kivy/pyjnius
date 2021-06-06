from cpython.version cimport PY_MAJOR_VERSION


def cast(destclass, obj):
    cdef JavaClass jc
    cdef JavaClass jobj = obj
    from .reflect import autoclass
    if (PY_MAJOR_VERSION < 3 and isinstance(destclass, base_string)) or \
          (PY_MAJOR_VERSION >=3 and isinstance(destclass, str)):
        jc = autoclass(destclass)(noinstance=True)
    else:
        jc = destclass(noinstance=True)
    jc.instanciate_from(jobj.j_self)
    return jc


def find_javaclass(namestr, raise_error=True):
    namestr = namestr.replace('.', '/')
    cdef bytes name = str_for_c(namestr)
    from .reflect import Class
    cdef JavaClass cls
    cdef jclass jc
    cdef JNIEnv *j_env = get_jnienv()
    cdef jthrowable

    jc = j_env[0].FindClass(j_env, name)
    if raise_error:
        check_exception(j_env)
    else:
        exc = j_env[0].ExceptionOccurred(j_env)
        if exc:
            j_env[0].ExceptionClear(j_env)
        return None

    cls = Class(noinstance=True)
    cls.instanciate_from(create_local_ref(j_env, jc))
    j_env[0].DeleteLocalRef(j_env, jc)
    return cls

