from future.builtins import range

cdef python_op(int op, object a, object b):
    if op == 0:
        return a < b
    elif op == 1:
        return a <= b
    elif op == 2:
        return a == b
    elif op == 3:
        return a >= b
    elif op == 4:
        return a > b
    elif op == 5:
        return a != b

cdef class ByteArray:
    cdef LocalRef _jobject
    cdef long _size
    cdef jbyte *_buf
    cdef jbyte[:] _arr

    def __cinit__(self):
        self._size = 0
        self._buf = NULL
        self._arr = None

    def __dealloc__(self):
        cdef JNIEnv *j_env
        if self._buf != NULL:
            j_env = get_jnienv()
            j_env[0].ReleaseByteArrayElements(j_env, self._jobject.obj, self._buf, 0)
            self._buf = NULL
        self._jobject = None

    cdef void set_buffer(self, JNIEnv *env, jobject obj, long size, jbyte *buf):
        if self._buf != NULL:
            raise Exception('Cannot call set_buffer() twice.')
        self._jobject = LocalRef()
        self._jobject.create(env, obj)
        self._size = size
        self._buf = buf
        self._arr = <jbyte[:size]>self._buf

    def __str__(self):
        return '<ByteArray size={} at 0x{}>'.format(
                self._size, id(self))

    def __len__(self):
        return self._size

    def __getitem__(self, n):
        if isinstance(n, slice):
            start, stop, step = n.indices(len(self))
            return [self._arr[i] for i in range(start, stop, step)]
        else: # for integer indices, do what we used to
            return self._arr[n]

    def __richcmp__(self, other, op):
        cdef ByteArray b_other
        if isinstance(other, (list, tuple)):
            return python_op(op, self.tolist(), other)
        elif isinstance(other, ByteArray):
            b_other = other
            return python_op(op, self.tostring(), other.tostring())
        else:
            return False

    def tolist(self):
        return list(self[:])

    def tostring(self):
        return self._buf[:self._size]
