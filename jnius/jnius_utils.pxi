cdef parse_definition(definition):
    # not a function, just a field
    if definition[0] != '(':
        return definition, None

    # it's a function!
    argdef, ret = definition[1:].split(')')
    args = []

    while len(argdef):
        c = argdef[0]

        # read the array char
        prefix = ''
        if c == '[':
            prefix = c
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
    cdef jthrowable exc = j_env[0].ExceptionOccurred(j_env)
    if exc:
        j_env[0].ExceptionDescribe(j_env)
        j_env[0].ExceptionClear(j_env)
        raise JavaException('JVM exception occured')


cdef dict assignable_from = {}
cdef void check_assignable_from(JNIEnv *env, JavaClass jc, bytes signature) except *:
    cdef jclass cls

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
        cls = env[0].FindClass(env, signature)
        if cls == NULL:
            raise JavaException('Unable to found the class for {0!r}'.format(
                signature))

        result = bool(env[0].IsAssignableFrom(env, jc.j_cls, cls))
        env[0].ExceptionDescribe(env)
        env[0].ExceptionClear(env)
        assignable_from[(jc.__javaclass__, signature)] = bool(result)

    if result is False:
        raise JavaException('Invalid instance of {0!r} passed for a {1!r}'.format(
            jc.__javaclass__, signature))


cdef bytes lookup_java_object_name(JNIEnv *j_env, jobject j_obj):
    cdef jclass jcls = j_env[0].GetObjectClass(j_env, j_obj)
    cdef jclass jcls2 = j_env[0].GetObjectClass(j_env, jcls)
    cdef jmethodID jmeth = j_env[0].GetMethodID(j_env, jcls2, 'getName', '()Ljava/lang/String;')
    cdef jobject js = j_env[0].CallObjectMethod(j_env, jcls, jmeth)
    name = convert_jobject_to_python(j_env, b'Ljava/lang/String;', js)
    j_env[0].DeleteLocalRef(j_env, js)
    j_env[0].DeleteLocalRef(j_env, jcls)
    j_env[0].DeleteLocalRef(j_env, jcls2)
    return name.replace('.', '/')


cdef int calculate_score(sign_args, args, is_varargs=False) except *:
    cdef int index
    cdef int score = 0
    cdef bytes r
    cdef JavaClass jc

    if len(args) != len(sign_args) and not is_varargs:
        # if the number of arguments expected is not the same
        # as the number of arguments the method gets
        # it can not be the method we are looking for except
        # if the method has varargs aka. it takes
        # an undefined number of arguments
        return -1
    elif len(args) == len(sign_args) and not is_varargs:
        # if the method has the good number of arguments and
        # the method doesn't take varargs increment the score
        # so that it takes precedence over a method with the same
        # signature and varargs e.g.
        # (Integer, Integer) takes precedence over (Integer, Integer, Integer...)
        # and
        # (Integer, Integer, Integer) takes precedence over (Integer, Integer, Integer...)
        score += 10

    for index in range(len(sign_args)):
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

        if r == 'S' or r == 'I' or r == 'J':
            if isinstance(arg, int):
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
            if r == 'java/lang/String' and isinstance(arg, basestring):
                score += 10
                continue

            # if it's a generic object, accept python string, or any java
            # class/object
            if r == 'java/lang/Object':
                if isinstance(arg, JavaClass) or isinstance(arg, JavaObject):
                    score += 10
                    continue
                elif isinstance(arg, basestring):
                    score += 5
                    continue
                return -1

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

            if (r == '[B' or r == '[C') and isinstance(arg, basestring):
                score += 10
                continue

            if r == '[B' and isinstance(arg, ByteArray):
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
