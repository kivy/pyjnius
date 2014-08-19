
def cast(destclass, obj):
    cdef JavaClass jc
    cdef JavaClass jobj = obj
    from .reflect import autoclass
    if isinstance(destclass, str):
        jc = autoclass(destclass)(noinstance=True)
    else:
        jc = destclass(noinstance=True)
    jc.instanciate_from(jobj.j_self)
    return jc

def find_javaclass(str name):
    from .reflect import Class
    cdef JavaClass cls
    cdef jclass jc
    cdef JNIEnv *j_env = get_jnienv()

    name = name.replace('.', '/')

    jc = j_env[0].FindClass(j_env, <bytes>name.encode('utf-8'))
    if jc == NULL:
        raise JavaException('Class not found {0!r}'.format(name))

    cls = Class(noinstance=True)
    cls.instanciate_from(create_local_ref(j_env, jc))
    return cls

