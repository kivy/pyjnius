cdef str_for_c(s):
     if PY2:
        if isinstance(s, unicode):
            return s.encode('utf-8')
        else:
            return s
     else:
        return s.encode('utf-8')

cdef items_compat(d):
     if not PY2:
         return d.items()
     else:
        return d.iteritems()                

cdef parse_definition(definition):
    # not a function, just a field
    if definition[0] != '(':
        return definition, None

    # it's a function!
    argdef, ret = definition[1:].split(')')
    args = []

    while len(argdef):
        c = argdef[0]

        # read the array char(s)
        prefix = ''
        while c == '[':
            prefix += c
            argdef = argdef[1:]
            c = argdef[0]

        # native type
        if c in 'ZBCSIJFD':
            args.append(prefix + c)
            argdef = argdef[1:]
            continue

        # java class
        if c == 'L':
            c, argdef = argdef.split(';', 1)
            args.append(prefix + c + ';')
            continue

        raise Exception('Invalid "{}" character in definition "{}"'.format(
            c, definition[1:]))

    return ret, tuple(args)


cdef void check_exception(JNIEnv *j_env) except *:
    cdef jmethodID toString = NULL
    cdef jmethodID getCause = NULL
    cdef jmethodID getStackTrace = NULL
    cdef jmethodID getMessage = NULL
    cdef jstring e_msg
    cdef jboolean isCopy
    cdef jthrowable exc = j_env[0].ExceptionOccurred(j_env)
    cdef jclass cls_object = NULL
    cdef jclass cls_throwable = NULL
    if exc:
        # ExceptionDescribe always writes to stderr, preventing tidy exception
        # handling, so should only be for debugging
        # j_env[0].ExceptionDescribe(j_env)
        j_env[0].ExceptionClear(j_env)

        cls_object = j_env[0].FindClass(j_env, "java/lang/Object")
        cls_throwable = j_env[0].FindClass(j_env, "java/lang/Throwable")

        toString = j_env[0].GetMethodID(j_env, cls_object, "toString", "()Ljava/lang/String;");
        getMessage = j_env[0].GetMethodID(j_env, cls_throwable, "getMessage", "()Ljava/lang/String;");
        getCause = j_env[0].GetMethodID(j_env, cls_throwable, "getCause", "()Ljava/lang/Throwable;");
        getStackTrace = j_env[0].GetMethodID(j_env, cls_throwable, "getStackTrace", "()[Ljava/lang/StackTraceElement;");

        e_msg = j_env[0].CallObjectMethod(j_env, exc, getMessage);
        pymsg = None if e_msg == NULL else convert_jstring_to_python(j_env, e_msg)

        pystack = []
        _append_exception_trace_messages(j_env, pystack, exc, getCause, getStackTrace, toString)

        pyexcclass = lookup_java_object_name(j_env, exc).replace('/', '.')

        j_env[0].DeleteLocalRef(j_env, cls_object)
        j_env[0].DeleteLocalRef(j_env, cls_throwable)
        if e_msg != NULL:
            j_env[0].DeleteLocalRef(j_env, e_msg)
        j_env[0].DeleteLocalRef(j_env, exc)

        raise JavaException('JVM exception occurred: %s' % (pymsg if pymsg is not None else pyexcclass), pyexcclass, pymsg, pystack)


cdef void _append_exception_trace_messages(
    JNIEnv*      j_env,
    list         pystack,
    jthrowable   exc,
    jmethodID    mid_getCause,
    jmethodID    mid_getStackTrace,
    jmethodID    mid_toString):

    # Get the array of StackTraceElements.
    cdef jobjectArray frames = j_env[0].CallObjectMethod(j_env, exc, mid_getStackTrace)
    cdef jsize frames_length = j_env[0].GetArrayLength(j_env, frames)
    cdef jstring msg_obj
    cdef jobject frame
    cdef jthrowable cause

    # Add Throwable.toString() before descending stack trace messages.
    if frames != NULL:
        msg_obj = j_env[0].CallObjectMethod(j_env, exc, mid_toString)
        pystr = None if msg_obj == NULL else convert_jobject_to_python(j_env, <bytes> 'Ljava/lang/String;', msg_obj)
        # If this is not the top-of-the-trace then this is a cause.
        if len(pystack) > 0:
            pystack.append("Caused by:")
        pystack.append(pystr)
        if msg_obj != NULL:
            j_env[0].DeleteLocalRef(j_env, msg_obj)

    # Append stack trace messages if there are any.
    if frames_length > 0:
        for i in range(frames_length):
            # Get the string returned from the 'toString()' method of the next frame and append it to the error message.
            frame = j_env[0].GetObjectArrayElement(j_env, frames, i)
            msg_obj = j_env[0].CallObjectMethod(j_env, frame, mid_toString)
            pystr = None if msg_obj == NULL else convert_jobject_to_python(j_env, <bytes> 'Ljava/lang/String;', msg_obj)
            pystack.append(pystr)
            if msg_obj != NULL:
                j_env[0].DeleteLocalRef(j_env, msg_obj)
            j_env[0].DeleteLocalRef(j_env, frame)

    # If 'exc' has a cause then append the stack trace messages from the cause.
    if frames != NULL:
        cause = j_env[0].CallObjectMethod(j_env, exc, mid_getCause)
        if cause != NULL:
            _append_exception_trace_messages(j_env, pystack, cause,
                                             mid_getCause, mid_getStackTrace, mid_toString)
            j_env[0].DeleteLocalRef(j_env, cause)

    j_env[0].DeleteLocalRef(j_env, frames)


cdef dict assignable_from = {}
cdef int assignable_from_order = 0
cdef void check_assignable_from(JNIEnv *env, JavaClass jc, signature) except *:
    global assignable_from_order
    cdef jclass cls, clsA, clsB
    cdef jthrowable exc

    # first call, we need to get over the libart issue, which implemented
    # IsAssignableFrom the wrong way.
    # Ref: https://github.com/kivy/pyjnius/issues/92
    # Google Bug: https://android.googlesource.com/platform/art/+/1268b74%5E!/
    if assignable_from_order == 0:
        clsA = env[0].FindClass(env, "java/lang/String")
        clsB = env[0].FindClass(env, "java/lang/Object")
        if env[0].IsAssignableFrom(env, clsB, clsA):
            # Bug triggered, IsAssignableFrom said we can do things like:
            # String a = Object()
            assignable_from_order = -1
        else:
            assignable_from_order = 1

    # if we have a JavaObject, it's always ok.
    if signature == 'java/lang/Object':
        return

    # FIXME Android/libART specific check
    # check_jni.cc crash when calling the IsAssignableFrom with
    # org/jnius/NativeInvocationHandler java/lang/reflect/InvocationHandler
    # Because we know it's ok, just return here.
    if signature == 'java/lang/reflect/InvocationHandler' and \
        jc.__javaclass__ == 'org/jnius/NativeInvocationHandler':
        return

    # if the signature is a direct match, it's ok too :)
    if jc.__javaclass__ == signature:
        return

    # if we already did the test before, use the cache result!
    result = assignable_from.get((jc.__javaclass__, signature), None)
    if result is None:

        # we got an object that doesn't match with the signature
        # check if we can use it.
        s = str_for_c(signature)
        cls = env[0].FindClass(env, s)
        if cls == NULL:
            raise JavaException('Unable to found the class for {0!r}'.format(
                signature))

        if assignable_from_order == 1:
            result = bool(env[0].IsAssignableFrom(env, jc.j_cls, cls))
        else:
            result = bool(env[0].IsAssignableFrom(env, cls, jc.j_cls))

        exc = env[0].ExceptionOccurred(env)
        if exc:
            env[0].ExceptionDescribe(env)
            env[0].ExceptionClear(env)

        assignable_from[(jc.__javaclass__, signature)] = bool(result)

    if result is False:
        raise JavaException('Invalid instance of {0!r} passed for a {1!r}'.format(
            jc.__javaclass__, signature))


cdef lookup_java_object_name(JNIEnv *j_env, jobject j_obj):
    cdef jclass jcls = j_env[0].GetObjectClass(j_env, j_obj)
    cdef jclass jcls2 = j_env[0].GetObjectClass(j_env, jcls)
    cdef jmethodID jmeth = j_env[0].GetMethodID(j_env, jcls2, 'getName', '()Ljava/lang/String;')
    cdef jobject js = j_env[0].CallObjectMethod(j_env, jcls, jmeth)
    name = convert_jobject_to_python(j_env, 'Ljava/lang/String;', js)
    j_env[0].DeleteLocalRef(j_env, js)
    j_env[0].DeleteLocalRef(j_env, jcls)
    j_env[0].DeleteLocalRef(j_env, jcls2)
    return name.replace('.', '/')


cdef int calculate_score(sign_args, args, is_varargs=False) except *:
    cdef int index
    cdef int score = 0
    cdef JavaClass jc
    cdef int args_len = len(args)
    cdef int sign_args_len = len(sign_args)

    if args_len != sign_args_len and not is_varargs:
        # if the number of arguments expected is not the same
        # as the number of arguments the method gets
        # it can not be the method we are looking for except
        # if the method has varargs aka. it takes
        # an undefined number of arguments
        return -1
    elif args_len == sign_args_len and not is_varargs:
        # if the method has the good number of arguments and
        # the method doesn't take varargs increment the score
        # so that it takes precedence over a method with the same
        # signature and varargs e.g.
        # (Integer, Integer) takes precedence over (Integer, Integer, Integer...)
        # and
        # (Integer, Integer, Integer) takes precedence over (Integer, Integer, Integer...)
        score += 10

    for index in range(sign_args_len):
        r = sign_args[index]
        arg = args[index]

        if r == 'Z':
            if not isinstance(arg, bool):
                return -1
            score += 10
            continue

        if r == 'B':
            if not isinstance(arg, int):
                return -1
            score += 10
            continue

        if r == 'C':
            if not isinstance(arg, str) or len(arg) != 1:
                return -1
            score += 10
            continue

        if r == 'S' or r == 'I':
            if isinstance(arg, int) or (
                    (isinstance(arg, long) and arg < 2147483648)):
                score += 10
                continue
            elif isinstance(arg, float):
                score += 5
                continue
            else:
                return -1

        if r == 'J':
            if isinstance(arg, int) or isinstance(arg, long):
                score += 10
                continue
            elif isinstance(arg, float):
                score += 5
                continue
            else:
                return -1

        if r == 'F' or r == 'D':
            if isinstance(arg, int):
                score += 5
                continue
            elif isinstance(arg, float):
                score += 10
                continue
            else:
                return -1

        if r[0] == 'L':

            r = r[1:-1]

            if arg is None:
                score += 10
                continue

            # if it's a string, accept any python string
            if r == 'java/lang/String' and isinstance(arg, base_string) and PY2:
                score += 10
                continue

            if r == 'java/lang/String' and isinstance(arg, str) and not PY2:
                score += 10
                continue

            # if it's a generic object, accept python string, or any java
            # class/object
            if r == 'java/lang/Object':
                if isinstance(arg, (PythonJavaClass, JavaClass, JavaObject)):
                    score += 10
                    continue
                elif isinstance(arg, base_string):
                    score += 5
                    continue
                elif isinstance(arg, (list, tuple)):
                    score += 5
                    continue
                elif isinstance(arg, int):
                    score += 5
                    continue
                elif isinstance(arg, float):
                    score += 5
                    continue
                return -1

            # accept an autoclass class for java/lang/Class.
            if hasattr(arg, '__javaclass__') and r == 'java/lang/Class':
                score += 10
                continue

            # if we pass a JavaClass, ensure the definition is matching
            # XXX FIXME what if we use a subclass or something ?
            if isinstance(arg, JavaClass):
                jc = arg
                if jc.__javaclass__ == r:
                    score += 10
                else:
                    #try:
                    #    check_assignable_from(jc, r)
                    #except:
                    #    return -1
                    score += 5
                continue

            # always accept unknow object, but can be dangerous too.
            if isinstance(arg, JavaObject):
                score += 1
                continue

            if isinstance(arg, PythonJavaClass):
                score += 1
                continue

            # native type? not accepted
            return -1

        if r[0] == '[':

            if arg is None:
                score += 10
                continue

            if (r == '[B' or r == '[C') and isinstance(arg, base_string) and PY2:
                score += 10
                continue

            if (r == '[B') and isinstance(arg, bytes) and not PY2:
                score += 10
                continue

            if (r == '[C') and isinstance(arg, str) and not PY2:
                score += 10
                continue

            if r == '[B' and isinstance(arg, (bytearray, ByteArray)):
                score += 10
                continue

            if not isinstance(arg, (list, tuple)):
                return -1

            # calculate the score for our subarray
            if len(arg) > 0:
                # if there are supplemantal arguments we compute the score
                subscore = calculate_score([r[1:]] * len(arg), arg)
                if subscore == -1:
                    return -1
                # the supplemental arguments match the varargs arguments
                score += 10
                continue
            # else if there is no supplemental arguments
            # it might be the good method but there may be
            # a method with a better signature so we don't
            # change this method score
    return score
