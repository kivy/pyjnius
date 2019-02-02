from cpython.version cimport PY_MAJOR_VERSION
from cpython cimport PyUnicode_DecodeUTF16


cdef jstringy_arg(argtype):
    return argtype in ('Ljava/lang/String;',
                       'Ljava/lang/CharSequence;',
                       'Ljava/lang/Object;')

cdef void release_args(JNIEnv *j_env, tuple definition_args, jvalue *j_args, args) except *:
    # do the conversion from a Python object to Java from a Java definition
    cdef JavaObject jo
    cdef JavaClass jc
    cdef int index
    for index, argtype in enumerate(definition_args):
        py_arg = args[index]
        if argtype[0] == 'L':
            if py_arg is None:
                j_args[index].l = NULL
            if isinstance(py_arg, basestring) and \
                    jstringy_arg(argtype):
                j_env[0].DeleteLocalRef(j_env, j_args[index].l)
        elif argtype[0] == '[':
            ret = convert_jarray_to_python(j_env, argtype[1:], j_args[index].l)
            try:
                args[index][:] = ret
            except TypeError:
                pass
            j_env[0].DeleteLocalRef(j_env, j_args[index].l)

cdef void populate_args(JNIEnv *j_env, tuple definition_args, jvalue *j_args, args) except *:
    # do the conversion from a Python object to Java from a Java definition
    cdef JavaClassStorage jcs
    cdef JavaObject jo
    cdef JavaClass jc
    cdef PythonJavaClass pc
    cdef int index

    for index, argtype in enumerate(definition_args):
        py_arg = args[index]
        if argtype == 'Z':
            j_args[index].z = py_arg
        elif argtype == 'B':
            j_args[index].b = py_arg
        elif argtype == 'C':
            j_args[index].c = ord(py_arg)
        elif argtype == 'S':
            j_args[index].s = py_arg
        elif argtype == 'I':
            j_args[index].i = py_arg
        elif argtype == 'J':
            j_args[index].j = py_arg
        elif argtype == 'F':
            j_args[index].f = py_arg
        elif argtype == 'D':
            j_args[index].d = py_arg
        elif argtype[0] == 'L':
            if py_arg is None:
                j_args[index].l = NULL

            # numeric types
            elif isinstance(py_arg, (int, long)):
                j_args[index].l = convert_python_to_jobject(
                    j_env, 'Ljava/lang/Integer;', py_arg
                )
            elif isinstance(py_arg, float):
                j_args[index].l = convert_python_to_jobject(
                    j_env, 'Ljava/lang/Float;', py_arg
                )

            # string types
            elif isinstance(py_arg, base_string) and jstringy_arg(argtype):
                j_args[index].l = convert_pystr_to_java(
                    j_env, to_unicode(py_arg)
                )
            elif isinstance(py_arg, JavaClass):
                jc = py_arg
                check_assignable_from(j_env, jc, argtype[1:-1])
                j_args[index].l = jc.j_self.obj

            # objects
            elif isinstance(py_arg, JavaObject):
                jo = py_arg
                j_args[index].l = jo.obj
            elif isinstance(py_arg, MetaJavaClass):
                jcs = py_arg.__cls_storage
                j_args[index].l = jcs.j_cls
            elif isinstance(py_arg, PythonJavaClass):
                # from python class, get the proxy/python class
                pc = py_arg
                # get the java class
                jc = pc.j_self
                if jc is None:
                    pc._init_j_self_ptr()
                    jc = pc.j_self
                # get the localref
                j_args[index].l = jc.j_self.obj

            # implementation of Java class in Python (needs j_cls)
            elif isinstance(py_arg, type):
                jc = py_arg
                j_args[index].l = jc.j_cls

            # array
            elif isinstance(py_arg, (tuple, list)):
                j_args[index].l = convert_pyarray_to_java(j_env, argtype, py_arg)

            else:
                raise JavaException('Invalid python object for this '
                        'argument. Want {0!r}, got {1!r}'.format(
                            argtype[1:-1], py_arg))

        elif argtype[0] == '[':
            if py_arg is None:
                j_args[index].l = NULL
                continue
            if isinstance(py_arg, basestring) and PY_MAJOR_VERSION < 3:
                if argtype == '[B':
                    py_arg = map(ord, py_arg)
                elif argtype == '[C':
                    py_arg = list(py_arg)
            if isinstance(py_arg, str) and PY_MAJOR_VERSION >= 3 and argtype == '[C':
                py_arg = list(py_arg)
            if isinstance(py_arg, ByteArray) and argtype != '[B':
                raise JavaException(
                    'Cannot use ByteArray for signature {}'.format(argtype))
            if not isinstance(py_arg, (list, tuple, ByteArray, bytes, bytearray)):
                raise JavaException('Expecting a python list/tuple, got '
                        '{0!r}'.format(py_arg))
            j_args[index].l = convert_pyarray_to_java(
                    j_env, argtype[1:], py_arg)


cdef convert_jobject_to_python(JNIEnv *j_env, definition, jobject j_object):
    # Convert a Java Object to a Python object, according to the definition.
    # If the definition is a java/lang/Object, then try to determine what is it
    # exactly.
    r = definition[1:-1]
    cdef JavaObject ret_jobject
    cdef JavaClass ret_jc
    cdef jclass retclass
    cdef jmethodID retmeth

    # we got a generic object -> lookup for the real name instead.
    if r == 'java/lang/Object':
        r = definition = lookup_java_object_name(j_env, j_object)
        # print('cjtp:r {0} definition {1}'.format(r, definition))

    if definition[0] == '[':
        return convert_jarray_to_python(j_env, definition[1:], j_object)

    # XXX what about others native type?
    # It seem, in case of the proxy, that they are never passed directly,
    # and always passed as "class" type instead.
    # Ie, B would be passed as Ljava/lang/Character;

    # if we got a string, just convert back to Python str.
    if r in ('java/lang/String', 'java/lang/CharSequence'):
        if r == 'java/lang/CharSequence':
            # call toString()
            retclass = j_env[0].GetObjectClass(j_env, j_object)
            retmeth = j_env[0].GetMethodID(j_env, retclass, "toString", "()Ljava/lang/String;")
            string = <jstring> (j_env[0].CallObjectMethod(j_env, j_object, retmeth))
        else:
            string = <jstring>j_object
        return convert_jstring_to_python(j_env, string)

    # XXX should be deactivable from configuration
    # ie, user might not want autoconvertion of lang classes.
    if r == 'java/lang/Long':
        retclass = j_env[0].GetObjectClass(j_env, j_object)
        retmeth = j_env[0].GetMethodID(j_env, retclass, 'longValue', '()J')
        return j_env[0].CallLongMethod(j_env, j_object, retmeth)
    if r == 'java/lang/Integer':
        retclass = j_env[0].GetObjectClass(j_env, j_object)
        retmeth = j_env[0].GetMethodID(j_env, retclass, 'intValue', '()I')
        return j_env[0].CallIntMethod(j_env, j_object, retmeth)
    if r == 'java/lang/Float':
        retclass = j_env[0].GetObjectClass(j_env, j_object)
        retmeth = j_env[0].GetMethodID(j_env, retclass, 'floatValue', '()F')
        return j_env[0].CallFloatMethod(j_env, j_object, retmeth)
    if r == 'java/lang/Double':
        retclass = j_env[0].GetObjectClass(j_env, j_object)
        retmeth = j_env[0].GetMethodID(j_env, retclass, 'doubleValue', '()D')
        return j_env[0].CallDoubleMethod(j_env, j_object, retmeth)
    if r == 'java/lang/Short':
        retclass = j_env[0].GetObjectClass(j_env, j_object)
        retmeth = j_env[0].GetMethodID(j_env, retclass, 'shortValue', '()S')
        return j_env[0].CallShortMethod(j_env, j_object, retmeth)
    if r == 'java/lang/Boolean':
        retclass = j_env[0].GetObjectClass(j_env, j_object)
        retmeth = j_env[0].GetMethodID(j_env, retclass, 'booleanValue', '()Z')
        return j_env[0].CallBooleanMethod(j_env, j_object, retmeth)
    if r == 'java/lang/Byte':
        retclass = j_env[0].GetObjectClass(j_env, j_object)
        retmeth = j_env[0].GetMethodID(j_env, retclass, 'byteValue', '()B')
        return j_env[0].CallByteMethod(j_env, j_object, retmeth)
    if r == 'java/lang/Character':
        retclass = j_env[0].GetObjectClass(j_env, j_object)
        retmeth = j_env[0].GetMethodID(j_env, retclass, 'charValue', '()C')
        return ord(j_env[0].CallCharMethod(j_env, j_object, retmeth))

    if r not in jclass_register:
        if r.startswith('$Proxy'):
            # only for $Proxy on android, don't use autoclass. The dalvik vm is
            # not able to give us introspection on that one (FindClass return
            # NULL).
            from .reflect import Object
            ret_jc = Object(noinstance=True)
        else:
            from .reflect import autoclass
            ret_jc = autoclass(r.replace('/', '.'))(noinstance=True)
    else:
        ret_jc = jclass_register[r](noinstance=True)
    ret_jc.instanciate_from(create_local_ref(j_env, j_object))
    return ret_jc

cdef convert_jstring_to_python(JNIEnv *j_env, jstring j_string):
    cdef jchar *j_chars
    cdef jsize j_strlen
    cdef Py_ssize_t buffsize
    cdef unicode py_uni

    j_chars = j_env[0].GetStringChars(j_env, j_string, NULL)
    if j_chars == NULL:
        check_exception(j_env) # raise error as JavaException
    try:
        j_strlen = j_env[0].GetStringLength(j_env, j_string);

        buffsize = j_strlen * sizeof(jchar)
        # py_uni = (<char *>j_chars)[:buffsize].decode('utf-16')
        # Calling directly into c-api for utf-16 decoding due to Cython code gen
        # bug for utf-16: https://github.com/cython/cython/issues/1696
        py_uni = PyUnicode_DecodeUTF16(<char *>j_chars, buffsize, NULL, NULL)
    finally:
        j_env[0].ReleaseStringChars(j_env, j_string, j_chars)

    if PY_MAJOR_VERSION < 3:
        return py_uni.encode('utf-8')
    else:
        return py_uni

cdef convert_jarray_to_python(JNIEnv *j_env, definition, jobject j_object):
    cdef jboolean iscopy
    cdef jboolean *j_booleans
    cdef jbyte *j_bytes
    cdef jchar *j_chars
    cdef jshort *j_shorts
    cdef jint *j_ints
    cdef jlong *j_longs
    cdef jfloat *j_floats
    cdef jdouble *j_doubles
    cdef object ret = None
    cdef jsize array_size

    cdef int i
    cdef jobject j_object_item
    cdef char *c_str
    cdef bytes py_str
    cdef JavaObject ret_jobject
    cdef JavaClass ret_jc
    cdef ByteArray ret_as_bytearray

    if j_object == NULL:
        return None

    array_size = j_env[0].GetArrayLength(j_env, j_object)

    r = definition[0]
    if r == 'Z':
        j_booleans = j_env[0].GetBooleanArrayElements(
                j_env, j_object, &iscopy)
        ret = [(True if j_booleans[i] else False)
                for i in range(array_size)]
        j_env[0].ReleaseBooleanArrayElements(
                j_env, j_object, j_booleans, 0)

    elif r == 'B':
        j_bytes = j_env[0].GetByteArrayElements(
                j_env, j_object, &iscopy)
        ret_as_bytearray = ByteArray()
        ret_as_bytearray.set_buffer(j_env, j_object, array_size, j_bytes)
        return ret_as_bytearray

    elif r == 'C':
        j_chars = j_env[0].GetCharArrayElements(
                j_env, j_object, &iscopy)
        ret = [chr(<char>j_chars[i]) for i in range(array_size)]
        j_env[0].ReleaseCharArrayElements(
                j_env, j_object, j_chars, 0)

    elif r == 'S':
        j_shorts = j_env[0].GetShortArrayElements(
                j_env, j_object, &iscopy)
        ret = [(<short>j_shorts[i]) for i in range(array_size)]
        j_env[0].ReleaseShortArrayElements(
                j_env, j_object, j_shorts, 0)

    elif r == 'I':
        j_ints = j_env[0].GetIntArrayElements(
                j_env, j_object, &iscopy)
        ret = [(<int>j_ints[i]) for i in range(array_size)]
        j_env[0].ReleaseIntArrayElements(
                j_env, j_object, j_ints, 0)

    elif r == 'J':
        j_longs = j_env[0].GetLongArrayElements(
                j_env, j_object, &iscopy)
        ret = [(<long long>j_longs[i]) for i in range(array_size)]
        j_env[0].ReleaseLongArrayElements(
                j_env, j_object, j_longs, 0)

    elif r == 'F':
        j_floats = j_env[0].GetFloatArrayElements(
                j_env, j_object, &iscopy)
        ret = [(<float>j_floats[i]) for i in range(array_size)]
        j_env[0].ReleaseFloatArrayElements(
                j_env, j_object, j_floats, 0)

    elif r == 'D':
        j_doubles = j_env[0].GetDoubleArrayElements(
                j_env, j_object, &iscopy)
        ret = [(<double>j_doubles[i]) for i in range(array_size)]
        j_env[0].ReleaseDoubleArrayElements(
                j_env, j_object, j_doubles, 0)

    elif r == 'L':
        r = definition[1:-1]
        ret = []
        for i in range(array_size):
            j_object_item = j_env[0].GetObjectArrayElement(
                    j_env, j_object, i)
            if j_object_item == NULL:
                ret.append(None)
                continue
            obj = convert_jobject_to_python(j_env, definition, j_object_item)
            ret.append(obj)
            j_env[0].DeleteLocalRef(j_env, j_object_item)

    elif r == '[':
        r = definition[1:]
        ret = []
        for i in range(array_size):
            j_object_item = j_env[0].GetObjectArrayElement(
                    j_env, j_object, i)
            if j_object_item == NULL:
                ret.append(None)
                continue
            obj = convert_jarray_to_python(j_env, r, j_object_item)
            ret.append(obj)
            j_env[0].DeleteLocalRef(j_env, j_object_item)

    else:
        raise JavaException('Invalid return definition for array')

    return ret

cdef jobject convert_python_to_jobject(JNIEnv *j_env, definition, obj) except *:
    cdef jobject retobject, retsubobject
    cdef jclass retclass
    cdef jmethodID redmidinit = NULL
    cdef jvalue j_ret[1]
    cdef JavaClass jc
    cdef JavaObject jo
    cdef JavaClassStorage jcs
    cdef PythonJavaClass pc
    cdef int index

    if definition[0] == 'V':
        return NULL
    elif definition[0] == 'L':
        if obj is None:
            return NULL

        # string types
        elif isinstance(obj, base_string) and jstringy_arg(definition):
            return convert_pystr_to_java(j_env, to_unicode(obj))

        # numeric types
        elif isinstance(obj, (int, long)) and \
                definition in (
                    'Ljava/lang/Integer;',
                    'Ljava/lang/Number;',
                    'Ljava/lang/Long;',
                    'Ljava/lang/Object;'):
            j_ret[0].i = int(obj)
            retclass = j_env[0].FindClass(j_env, 'java/lang/Integer')
            retmidinit = j_env[0].GetMethodID(j_env, retclass, '<init>', '(I)V')
            retobject = j_env[0].NewObjectA(j_env, retclass, retmidinit, j_ret)
            return retobject
        elif isinstance(obj, float) and \
                definition in (
                    'Ljava/lang/Float;',
                    'Ljava/lang/Number;',
                    'Ljava/lang/Object;'):
            j_ret[0].f = obj
            retclass = j_env[0].FindClass(j_env, 'java/lang/Float')
            retmidinit = j_env[0].GetMethodID(j_env, retclass, '<init>', '(F)V')
            retobject = j_env[0].NewObjectA(j_env, retclass, retmidinit, j_ret)
            return retobject

        # implementation of Java class in Python (needs j_cls)
        elif isinstance(obj, type):
            jc = obj
            return jc.j_cls

        # objects
        elif isinstance(obj, JavaClass):
            jc = obj
            check_assignable_from(j_env, jc, definition[1:-1])
            return jc.j_self.obj
        elif isinstance(obj, JavaObject):
            jo = obj
            return jo.obj
        elif isinstance(obj, MetaJavaClass):
            jcs = obj.__cls_storage
            return jcs.j_cls
        elif isinstance(obj, PythonJavaClass):
            # from python class, get the proxy/python class
            pc = obj
            # get the java class
            jc = pc.j_self
            if jc is None:
                pc._init_j_self_ptr()
                jc = pc.j_self
            # get the localref
            return jc.j_self.obj

        # array
        elif isinstance(obj, (tuple, list)):
            return convert_pyarray_to_java(j_env, definition, obj)

        else:
            raise JavaException('Invalid python object for this '
                    'argument. Want {0!r}, got {1!r}'.format(
                        definition[1:-1], obj))

    elif definition[0] == '[':
        if PY_MAJOR_VERSION < 3:
            conversions = {
                int: 'I',
                bool: 'Z',
                long: 'J',
                float: 'F',
                unicode: 'Ljava/lang/String;',
                bytes: 'Ljava/lang/String;'
            }
        else:
            conversions = {
                int: 'I',
                bool: 'Z',
                long: 'J',
                float: 'F',
                unicode: 'Ljava/lang/String;',
                bytes: 'B'
            }
        retclass = j_env[0].FindClass(j_env, 'java/lang/Object')
        retobject = j_env[0].NewObjectArray(j_env, len(obj), retclass, NULL)
        for index, item in enumerate(obj):
            item_definition = conversions.get(type(item), definition[1:])
            retsubobject = convert_python_to_jobject(
                    j_env, item_definition, item)
            j_env[0].SetObjectArrayElement(j_env, retobject, index,
                    retsubobject)
            j_env[0].DeleteLocalRef(j_env, retsubobject)
        return retobject

    elif definition == 'B':
        retclass = j_env[0].FindClass(j_env, 'java/lang/Byte')
        retmidinit = j_env[0].GetMethodID(j_env, retclass, '<init>', '(B)V')
        j_ret[0].b = obj
    elif definition == 'S':
        retclass = j_env[0].FindClass(j_env, 'java/lang/Short')
        retmidinit = j_env[0].GetMethodID(j_env, retclass, '<init>', '(S)V')
        j_ret[0].s = obj
    elif definition == 'I':
        retclass = j_env[0].FindClass(j_env, 'java/lang/Integer')
        retmidinit = j_env[0].GetMethodID(j_env, retclass, '<init>', '(I)V')
        j_ret[0].i = int(obj)
    elif definition == 'J':
        retclass = j_env[0].FindClass(j_env, 'java/lang/Long')
        retmidinit = j_env[0].GetMethodID(j_env, retclass, '<init>', '(J)V')
        j_ret[0].j = obj
    elif definition == 'F':
        retclass = j_env[0].FindClass(j_env, 'java/lang/Float')
        retmidinit = j_env[0].GetMethodID(j_env, retclass, '<init>', '(F)V')
        j_ret[0].f = obj
    elif definition == 'D':
        retclass = j_env[0].FindClass(j_env, 'java/lang/Double')
        retmidinit = j_env[0].GetMethodID(j_env, retclass, '<init>', '(D)V')
        j_ret[0].d = obj
    elif definition == 'C':
        retclass = j_env[0].FindClass(j_env, 'java/lang/Char')
        retmidinit = j_env[0].GetMethodID(j_env, retclass, '<init>', '(C)V')
        j_ret[0].c = ord(obj)
    elif definition == 'Z':
        retclass = j_env[0].FindClass(j_env, 'java/lang/Boolean')
        retmidinit = j_env[0].GetMethodID(j_env, retclass, '<init>', '(Z)V')
        j_ret[0].z = 1 if obj else 0
    else:
        assert(0)

    assert(retclass != NULL)
    # XXX do we need a globalref or something ?
    retobject = j_env[0].NewObjectA(j_env, retclass, retmidinit, j_ret)
    return retobject

cdef jstring convert_pystr_to_java(JNIEnv *j_env, unicode py_uni) except NULL:
    cdef bytes py_bytes
    cdef jstring j_str
    cdef jsize j_strlen
    cdef char *buff

    py_bytes = py_uni.encode('utf-16')
    # skip byte-order mark
    buff = (<char *>py_bytes) + sizeof(jchar)
    j_strlen = len(py_bytes) / sizeof(jchar) - 1
    j_str = j_env[0].NewString(j_env, <jchar *>buff, j_strlen)

    if j_str == NULL:
        check_exception(j_env) # raise error as JavaException
    return j_str

cdef jobject convert_pyarray_to_java(JNIEnv *j_env, definition, pyarray) except *:
    cdef jobject ret = NULL
    cdef jobject nested = NULL
    cdef int array_size = len(pyarray)
    cdef int i
    cdef unsigned char c_tmp
    cdef jboolean j_boolean
    cdef jbyte j_byte
    cdef jchar j_char
    cdef jshort j_short
    cdef jint j_int
    cdef jlong j_long
    cdef jfloat j_float
    cdef jdouble j_double
    cdef jstring j_string
    cdef jclass j_class
    cdef JavaObject jo
    cdef JavaClass jc

    cdef ByteArray a_bytes


    if definition == 'Ljava/lang/Object;' and len(pyarray) > 0:
        # then the method will accept any array type as param
        # let's be as precise as we can
        if PY_MAJOR_VERSION < 3:
            conversions = {
                int: 'I',
                bool: 'Z',
                long: 'J',
                float: 'F',
                basestring: 'Ljava/lang/String;',
            }
        else:
            conversions = {
                int: 'I',
                bool: 'Z',
                long: 'J',
                float: 'F',
                bytes: 'B',
                str: 'Ljava/lang/String;',
            }
        for _type, override in conversions.iteritems():
            if isinstance(pyarray[0], _type):
                definition = override
                break

    if definition == 'Z':
        ret = j_env[0].NewBooleanArray(j_env, array_size)
        for i in range(array_size):
            j_boolean = 1 if pyarray[i] else 0
            j_env[0].SetBooleanArrayRegion(j_env,
                    ret, i, 1, &j_boolean)

    elif definition == 'B':
        ret = j_env[0].NewByteArray(j_env, array_size)
        if isinstance(pyarray, ByteArray):
            a_bytes = pyarray
            j_env[0].SetByteArrayRegion(j_env,
                ret, 0, array_size, <const_jbyte *>a_bytes._buf)
        else:
            for i in range(array_size):
                c_tmp = pyarray[i]
                j_byte = <signed char>c_tmp
                j_env[0].SetByteArrayRegion(j_env,
                        ret, i, 1, &j_byte)

    elif definition == 'C':
        ret = j_env[0].NewCharArray(j_env, array_size)
        for i in range(array_size):
            j_char = ord(pyarray[i])
            j_env[0].SetCharArrayRegion(j_env,
                    ret, i, 1, &j_char)

    elif definition == 'S':
        ret = j_env[0].NewShortArray(j_env, array_size)
        for i in range(array_size):
            j_short = pyarray[i]
            j_env[0].SetShortArrayRegion(j_env,
                    ret, i, 1, &j_short)

    elif definition == 'I':
        ret = j_env[0].NewIntArray(j_env, array_size)
        for i in range(array_size):
            j_int = pyarray[i]
            j_env[0].SetIntArrayRegion(j_env,
                    ret, i, 1, <const_jint *>&j_int)

    elif definition == 'J':
        ret = j_env[0].NewLongArray(j_env, array_size)
        for i in range(array_size):
            j_long = pyarray[i]
            j_env[0].SetLongArrayRegion(j_env,
                    ret, i, 1, &j_long)

    elif definition == 'F':
        ret = j_env[0].NewFloatArray(j_env, array_size)
        for i in range(array_size):
            j_float = pyarray[i]
            j_env[0].SetFloatArrayRegion(j_env,
                    ret, i, 1, &j_float)

    elif definition == 'D':
        ret = j_env[0].NewDoubleArray(j_env, array_size)
        for i in range(array_size):
            j_double = pyarray[i]
            j_env[0].SetDoubleArrayRegion(j_env,
                    ret, i, 1, &j_double)

    elif definition[0] == 'L':
        defstr = str_for_c(definition[1:-1])
        j_class = j_env[0].FindClass(j_env, <bytes>defstr)

        if j_class == NULL:
            raise JavaException(
                'Cannot create array with a class not '
                'found {0!r}'.format(definition[1:-1])
            )

        ret = j_env[0].NewObjectArray(
            j_env, array_size, j_class, NULL
        )

        # iterate over each Python array element
        # and add it to Object[].
        for i in range(array_size):
            arg = pyarray[i]

            if arg is None:
                j_env[0].SetObjectArrayElement(
                    j_env, <jobjectArray>ret, i, NULL
                )

            elif isinstance(arg, basestring):
                j_string = convert_pystr_to_java(j_env, to_unicode(arg))
                j_env[0].SetObjectArrayElement(
                    j_env, <jobjectArray>ret, i, j_string
                )
                j_env[0].DeleteLocalRef(j_env, j_string)

            # isinstance(arg, type) will return False
            # ...and it's really weird
            elif isinstance(arg, (tuple, list)):
                nested = convert_pyarray_to_java(
                    j_env, definition, arg
                )
                j_env[0].SetObjectArrayElement(
                    j_env, <jobjectArray>ret, i, nested
                )
                j_env[0].DeleteLocalRef(j_env, nested)

            # no local refs to delete for class, type and object
            elif isinstance(arg, JavaClass):
                jc = arg
                check_assignable_from(j_env, jc, definition[1:-1])
                j_env[0].SetObjectArrayElement(
                    j_env, <jobjectArray>ret, i, jc.j_self.obj
                )

            elif isinstance(arg, type):
                jc = arg
                j_env[0].SetObjectArrayElement(
                    j_env, <jobjectArray>ret, i, jc.j_cls
                )

            elif isinstance(arg, JavaObject):
                jo = arg
                j_env[0].SetObjectArrayElement(
                    j_env, <jobjectArray>ret, i, jo.obj
                )

            else:
                raise JavaException(
                    'Invalid variable {!r} used for L array {!r}'.format(
                        pyarray, definition
                    )
                )

    elif definition[0] == '[':
        subdef = definition[1:]
        eproto = convert_pyarray_to_java(j_env, subdef, pyarray[0])
        ret = j_env[0].NewObjectArray(
                j_env, array_size, j_env[0].GetObjectClass(j_env, eproto), NULL)
        j_env[0].SetObjectArrayElement(
                    j_env, <jobjectArray>ret, 0, eproto)
        j_env[0].DeleteLocalRef(j_env, eproto)
        for i in range(1, array_size):
            j_elem = convert_pyarray_to_java(j_env, subdef, pyarray[i])
            j_env[0].SetObjectArrayElement(j_env, <jobjectArray>ret, i, j_elem)
            j_env[0].DeleteLocalRef(j_env, j_elem)

    else:
        raise JavaException(
            'Invalid array definition {!r} for variable {!r}'.format(
                definition, pyarray
            )
        )

    return <jobject>ret
