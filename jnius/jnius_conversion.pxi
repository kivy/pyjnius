cdef void release_args(JNIEnv *j_env, list definition_args, jvalue *j_args, args) except *:
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
                    argtype in ('Ljava/lang/String;', 'Ljava/lang/Object;'):
                j_env[0].DeleteLocalRef(j_env, j_args[index].l)
        elif argtype[0] == '[':
            j_env[0].DeleteLocalRef(j_env, j_args[index].l)


cdef void populate_args(JNIEnv *j_env, list definition_args, jvalue *j_args, args) except *:
    # do the conversion from a Python object to Java from a Java definition
    cdef JavaObject jo
    cdef JavaClass jc
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
            elif isinstance(py_arg, basestring) and \
                    argtype in ('Ljava/lang/String;', 'Ljava/lang/Object;'):
                j_args[index].l = j_env[0].NewStringUTF(
                        j_env, <char *><bytes>py_arg)
            elif isinstance(py_arg, JavaClass):
                jc = py_arg
                check_assignable_from(j_env, jc, argtype[1:-1])
                j_args[index].l = jc.j_self.obj
            elif isinstance(py_arg, JavaObject):
                jo = py_arg
                j_args[index].l = jo.obj
                raise JavaException('JavaObject needed for argument '
                        '{0}'.format(index))
            else:
                raise JavaException('Invalid python object for this '
                        'argument. Want {0!r}, got {1!r}'.format(
                            argtype[1:-1], py_arg))
        elif argtype[0] == '[':
            if not isinstance(py_arg, list) and \
                    not isinstance(py_arg, tuple):
                raise JavaException('Expecting a python list/tuple, got '
                        '{0!r}'.format(py_arg))

            j_args[index].l = convert_pyarray_to_java(
                    j_env, argtype[1:], py_arg)


cdef convert_jobject_to_python(JNIEnv *j_env, bytes definition, jobject j_object):
    # Convert a Java Object to a Python object, according to the definition.
    # If the definition is a java/lang/Object, then try to determine what is it
    # exactly.
    cdef char *c_str
    cdef bytes py_str
    cdef bytes r = definition[1:-1]
    cdef JavaObject ret_jobject
    cdef JavaClass ret_jc

    # we got a generic object -> lookup for the real name instead.
    if r == 'java/lang/Object':
        r = lookup_java_object_name(j_env, j_object)

    # if we got a string, just convert back to Python str.
    if r == 'java/lang/String':
        c_str = <char *>j_env[0].GetStringUTFChars(j_env, j_object, NULL)
        py_str = <bytes>c_str
        j_env[0].ReleaseStringUTFChars(j_env, j_object, c_str)
        return py_str

    if r not in jclass_register:
        from reflect import autoclass
        ret_jc = autoclass(r.replace('/', '.'))(noinstance=True)
    else:
        ret_jc = jclass_register[r](noinstance=True)
    ret_jc.instanciate_from(create_local_ref(j_env, j_object))
    return ret_jc


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

    if j_object == NULL:
        return None

    array_size = j_env[0].GetArrayLength(j_env, j_object)

    r = definition[0]
    if r == 'Z':
        j_booleans = j_env[0].GetBooleanArrayElements(
                j_env, j_object, &iscopy)
        ret = [(True if j_booleans[i] else False)
                for i in range(array_size)]
        if iscopy:
            j_env[0].ReleaseBooleanArrayElements(
                    j_env, j_object, j_booleans, 0)

    elif r == 'B':
        j_bytes = j_env[0].GetByteArrayElements(
                j_env, j_object, &iscopy)
        ret = [(<char>j_bytes[i]) for i in range(array_size)]
        if iscopy:
            j_env[0].ReleaseByteArrayElements(
                    j_env, j_object, j_bytes, 0)

    elif r == 'C':
        j_chars = j_env[0].GetCharArrayElements(
                j_env, j_object, &iscopy)
        ret = [chr(<char>j_chars[i]) for i in range(array_size)]
        if iscopy:
            j_env[0].ReleaseCharArrayElements(
                    j_env, j_object, j_chars, 0)

    elif r == 'S':
        j_shorts = j_env[0].GetShortArrayElements(
                j_env, j_object, &iscopy)
        ret = [(<short>j_shorts[i]) for i in range(array_size)]
        if iscopy:
            j_env[0].ReleaseShortArrayElements(
                    j_env, j_object, j_shorts, 0)

    elif r == 'I':
        j_ints = j_env[0].GetIntArrayElements(
                j_env, j_object, &iscopy)
        ret = [(<int>j_ints[i]) for i in range(array_size)]
        if iscopy:
            j_env[0].ReleaseIntArrayElements(
                    j_env, j_object, j_ints, 0)

    elif r == 'J':
        j_longs = j_env[0].GetLongArrayElements(
                j_env, j_object, &iscopy)
        ret = [(<long>j_longs[i]) for i in range(array_size)]
        if iscopy:
            j_env[0].ReleaseLongArrayElements(
                    j_env, j_object, j_longs, 0)

    elif r == 'F':
        j_floats = j_env[0].GetFloatArrayElements(
                j_env, j_object, &iscopy)
        ret = [(<float>j_floats[i]) for i in range(array_size)]
        if iscopy:
            j_env[0].ReleaseFloatArrayElements(
                    j_env, j_object, j_floats, 0)

    elif r == 'D':
        j_doubles = j_env[0].GetDoubleArrayElements(
                j_env, j_object, &iscopy)
        ret = [(<double>j_doubles[i]) for i in range(array_size)]
        if iscopy:
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
    else:
        raise JavaException('Invalid return definition for array')

    return ret


cdef jobject convert_pyarray_to_java(JNIEnv *j_env, definition, pyarray) except *:
    cdef jobject ret = NULL
    cdef int array_size = len(pyarray)
    cdef int i
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

    if definition == 'Z':
        ret = j_env[0].NewBooleanArray(j_env, array_size)
        for i in range(array_size):
            j_boolean = 1 if pyarray[i] else 0
            j_env[0].SetBooleanArrayRegion(j_env,
                    ret, i, 1, &j_boolean)

    elif definition == 'B':
        ret = j_env[0].NewByteArray(j_env, array_size)
        for i in range(array_size):
            j_byte = pyarray[i]
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
        j_class = j_env[0].FindClass(
                j_env, <bytes>definition[1:-1])
        if j_class == NULL:
            raise JavaException('Cannot create array with a class not '
                    'found {0!r}'.format(definition[1:-1]))
        ret = j_env[0].NewObjectArray(
                j_env, array_size, j_class, NULL)
        for i in range(array_size):
            arg = pyarray[i]
            if arg is None:
                j_env[0].SetObjectArrayElement(
                        j_env, <jobjectArray>ret, i, NULL)
            elif isinstance(arg, basestring) and \
                    definition == 'Ljava/lang/String;':
                j_string = j_env[0].NewStringUTF(
                        j_env, <bytes>arg)
                j_env[0].SetObjectArrayElement(
                        j_env, <jobjectArray>ret, i, j_string)
            elif isinstance(arg, JavaClass):
                jc = arg
                check_assignable_from(j_env, jc, definition[1:-1])
                j_env[0].SetObjectArrayElement(
                        j_env, <jobjectArray>ret, i, jc.j_self.obj)
            elif isinstance(arg, JavaObject):
                jo = arg
                j_env[0].SetObjectArrayElement(
                        j_env, <jobjectArray>ret, i, jo.obj)
            else:
                raise JavaException('Invalid variable used for L array')

    else:
        raise JavaException('Invalid array definition')

    return <jobject>ret
