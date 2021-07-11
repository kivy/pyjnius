cdef class LocalRef:
    cdef jobject obj

    def __cinit__(self):
        self.obj = NULL

    def __dealloc__(self):
        cdef JNIEnv *j_env
        if self.obj != NULL:
            j_env = get_jnienv()
            j_env[0].DeleteGlobalRef(j_env, self.obj)
        self.obj = NULL

    cdef void create(self, JNIEnv *env, jobject obj) except *:
        self.obj = env[0].NewGlobalRef(env, obj)

    def __repr__(self):
        return '<LocalRef obj=0x{0:x} at 0x{1:x}>'.format(
            <long><void *>self.obj, id(self))


cdef LocalRef create_local_ref(JNIEnv *env, jobject obj):
    cdef LocalRef ret = LocalRef()
    ret.create(env, obj)
    return ret

