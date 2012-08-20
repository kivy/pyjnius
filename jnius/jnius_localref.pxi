
cdef class LocalRef:
    cdef jobject obj
    cdef JNIEnv *env

    def __cinit__(self):
        self.obj = NULL
        self.env = NULL

    def __dealloc__(self):
        if self.obj != NULL:
            self.env[0].DeleteLocalRef(self.env, self.obj)
        self.obj = NULL
        self.env = NULL

    cdef void create(self, JNIEnv *env, jobject obj):
        self.env = env
        self.obj = env[0].NewLocalRef(env, obj)


cdef LocalRef create_local_ref(JNIEnv *env, jobject obj):
    cdef LocalRef ret = LocalRef()
    ret.create(env, obj)
    return ret

