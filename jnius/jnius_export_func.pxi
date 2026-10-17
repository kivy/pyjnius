from libc.stdlib cimport getenv

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


def find_javaclass(namestr):
    namestr = namestr.replace('.', '/')
    cdef bytes name = str_for_c(namestr)
    from .reflect import Class
    cdef JavaClass cls
    cdef jclass jc
    cdef JNIEnv *j_env = get_jnienv()

    jc = j_env[0].FindClass(j_env, name)
    try:
        check_exception(j_env)
    except JavaException as e:
        jc = load_class_from_dex_jni(name)
        if jc == NULL:
            raise

    cls = Class(noinstance=True)
    cls.instanciate_from(create_local_ref(j_env, jc))
    j_env[0].DeleteLocalRef(j_env, jc)
    return cls

cdef jclass load_class_from_dex_jni(const char* class_name):
    cdef JNIEnv *j_env = get_jnienv()
    cdef jclass dex_class_loader_class
    cdef jmethodID load_class_id
    cdef jobject dex_class_loader
    cdef jstring j_class_name
    cdef jclass loaded_class

    dex_class_loader = get_dex_class_loader()
    if dex_class_loader == NULL:
        return NULL

    load_class_id = j_env[0].GetMethodID(j_env, j_env[0].GetObjectClass(j_env, dex_class_loader), b"loadClass", b"(Ljava/lang/String;)Ljava/lang/Class;")
    check_exception(j_env)

    j_class_name = j_env[0].NewStringUTF(j_env, class_name)
    loaded_class = <jclass>j_env[0].CallObjectMethod(j_env, dex_class_loader, load_class_id, j_class_name)
    try:
        check_exception(j_env)
    finally:
        j_env[0].DeleteLocalRef(j_env, j_class_name)

    return loaded_class

cdef get_dex_class_loader_python():
    cdef jobject loader = get_dex_class_loader()
    cdef JNIEnv *j_env = get_jnienv()
    obj = convert_jobject_to_python(j_env, <bytes> 'Ldalvik/system/DexClassLoader;', loader)
    return obj

cdef jobject get_dex_class_loader():
    cdef JNIEnv *j_env = get_jnienv()
    cdef jclass dex_class_loader_class
    cdef jmethodID constructor_id
    cdef jobject dex_class_loader
    cdef jstring j_dex_path
    cdef const char* dex_path
    global dex_class_loader_instance

    if dex_class_loader_instance != NULL:
        return dex_class_loader_instance

    cdef const char* varname = "PYJNIUS_DEX_PATH"
    dex_path = getenv(varname)
    if dex_path == NULL:
        return NULL

    import os

    dex_paths = dex_path.decode('utf-8').split(':')
    for path in dex_paths:
        if not os.access(path, os.R_OK):
            raise JavaException(f"DEX file not accessible: {path}")

    dex_class_loader_class = j_env[0].FindClass(j_env, b"dalvik/system/DexClassLoader")
    check_exception(j_env)

    constructor_id = j_env[0].GetMethodID(j_env, dex_class_loader_class, b"<init>", b"(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/ClassLoader;)V")
    check_exception(j_env)

    j_dex_path = j_env[0].NewStringUTF(j_env, dex_path)
    dex_class_loader = j_env[0].NewObject(j_env, dex_class_loader_class, constructor_id, j_dex_path, NULL, NULL, NULL)
    try:
        check_exception(j_env)
    finally:
        j_env[0].DeleteLocalRef(j_env, j_dex_path)

    dex_class_loader_instance = dex_class_loader
    return dex_class_loader_instance

cdef jobject dex_class_loader_instance = NULL
