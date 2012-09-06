cdef extern from "stdarg.h":
    ctypedef struct va_list:
        pass
    ctypedef struct fake_type:
        pass
    void va_start(va_list, void* arg)
    void* va_arg(va_list, fake_type)
    void va_end(va_list)
    fake_type bool_type "int"
    fake_type byte_type "char" # can i really do this?
    fake_type char_type "char"
    fake_type int_type "int"
    fake_type short_type "short"
    fake_type long_type "long"
    fake_type float_type "float"
    fake_type double_type "double"
    fake_type pointer_type "void*"


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

    return ret, args


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
        env[0].ExceptionClear(env)
        print 'CHECK FOR', jc.__javaclass__, signature, result
        assignable_from[(jc.__javaclass__, signature)] = bool(result)

    if result is False:
        raise JavaException('Invalid instance of {0!r} passed for a {1!r}'.format(
            jc.__javaclass__, signature))


cdef bytes lookup_java_object_name(JNIEnv *j_env, jobject j_obj):
    from reflect import ensureclass, autoclass
    ensureclass('java.lang.Object')
    ensureclass('java.lang.Class')
    cdef JavaClass obj = autoclass('java.lang.Object')(noinstance=True)
    obj.instanciate_from(create_local_ref(j_env, j_obj))
    cls = obj.getClass()
    name = cls.getName()
    ensureclass(name)
    return name.replace('.', '/')


cdef int calculate_score(sign_args, args) except *:
    cdef int index
    cdef int score = 0
    cdef bytes r
    cdef JavaClass jc

    if len(args) != len(sign_args):
        return -1

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

            # native type? not accepted
            return -1

        if r[0] == '[':

            if arg is None:
                return 10

            if not isinstance(arg, tuple) and not isinstance(arg, list):
                return -1

            # calculate the score for our subarray
            subscore = calculate_score([r[1:]] * len(arg), arg)
            if subscore == -1:
                return -1

            # look like the array is matching, accept it.
            score += 10
            continue

    return score


cdef class GenericNativeWrapper(object):
    """
    This class is to be used to register python method as methods of
    JavaObjects using RegisterNatives
    """
    cdef JNIEnv* j_env
    cdef args

    def __cinit__(self, j_env, definition, callback):
        self.j_env = NULL

    def __init__(self, j_env, definition, callback):
        self.callback = callback
        self.definitions = parse_definition(definition)[1]

    cdef void call_void(self, ...):
        cdef va_list j_args
        cdef int n
        cdef void* l

        args = []

        va_start(j_args, <void*>self)

        for d in self.definitions:
            if d == 'Z':
                args.append(<bint>va_arg(j_args, bool_type))
            elif d == 'B':
                args.append(<char>va_arg(j_args, char_type))
            elif d == 'C':
                args.append(<char>va_arg(j_args, byte_type))
            elif d == 'S':
                args.append(<short>va_arg(j_args, short_type))
            elif d == 'I':
                args.append(<int>va_arg(j_args, int_type))
            elif d == 'J':
                args.append(<long>va_arg(j_args, long_type))
            elif d == 'F':
                args.append(<float>va_arg(j_args, float_type))
            elif d == 'D':
                args.append(<double>va_arg(j_args, double_type))
            else: # == L, java object
                l = <void*>va_arg(j_args, pointer_type)
                args.append(convert_jobject_to_python(self.j_env, d, l))

        va_end(j_args)

        self.callback(*args)

    # XXX define call_int/call_bool/call_char/... and friends on the
    # same model, and "array of" variants

    cdef bint call_bint(self, ...):
        cdef va_list j_args
        cdef int n
        cdef void* l

        args = []

        va_start(j_args, <void*>self)

        for d in self.definitions:
            if d == 'Z':
                args.append(<bint>va_arg(j_args, bool_type))
            elif d == 'B':
                args.append(<char>va_arg(j_args, char_type))
            elif d == 'C':
                args.append(<char>va_arg(j_args, byte_type))
            elif d == 'S':
                args.append(<short>va_arg(j_args, short_type))
            elif d == 'I':
                args.append(<int>va_arg(j_args, int_type))
            elif d == 'J':
                args.append(<long>va_arg(j_args, long_type))
            elif d == 'F':
                args.append(<float>va_arg(j_args, float_type))
            elif d == 'D':
                args.append(<double>va_arg(j_args, double_type))
            else: # == L, java object
                l = <void*>va_arg(j_args, pointer_type)
                args.append(convert_jobject_to_python(self.j_env, d, l))

        va_end(j_args)

        return self.callback(*args)


    cdef char call_byte(self, ...):
        cdef va_list j_args
        cdef int n
        cdef void* l

        args = []

        va_start(j_args, <void*>self)

        for d in self.definitions:
            if d == 'Z':
                args.append(<bint>va_arg(j_args, bool_type))
            elif d == 'B':
                args.append(<char>va_arg(j_args, char_type))
            elif d == 'C':
                args.append(<char>va_arg(j_args, byte_type))
            elif d == 'S':
                args.append(<short>va_arg(j_args, short_type))
            elif d == 'I':
                args.append(<int>va_arg(j_args, int_type))
            elif d == 'J':
                args.append(<long>va_arg(j_args, long_type))
            elif d == 'F':
                args.append(<float>va_arg(j_args, float_type))
            elif d == 'D':
                args.append(<double>va_arg(j_args, double_type))
            else: # == L, java object
                l = <void*>va_arg(j_args, pointer_type)
                args.append(convert_jobject_to_python(self.j_env, d, l))

        va_end(j_args)

        return self.callback(*args)


    cdef char call_char(self, ...):
        cdef va_list j_args
        cdef int n
        cdef void* l

        args = []

        va_start(j_args, <void*>self)

        for d in self.definitions:
            if d == 'Z':
                args.append(<bint>va_arg(j_args, bool_type))
            elif d == 'B':
                args.append(<char>va_arg(j_args, char_type))
            elif d == 'C':
                args.append(<char>va_arg(j_args, byte_type))
            elif d == 'S':
                args.append(<short>va_arg(j_args, short_type))
            elif d == 'I':
                args.append(<int>va_arg(j_args, int_type))
            elif d == 'J':
                args.append(<long>va_arg(j_args, long_type))
            elif d == 'F':
                args.append(<float>va_arg(j_args, float_type))
            elif d == 'D':
                args.append(<double>va_arg(j_args, double_type))
            else: # == L, java object
                l = <void*>va_arg(j_args, pointer_type)
                args.append(convert_jobject_to_python(self.j_env, d, l))

        va_end(j_args)

        return self.callback(*args)


    cdef short call_short(self, ...):
        cdef va_list j_args
        cdef int n
        cdef void* l

        args = []

        va_start(j_args, <void*>self)

        for d in self.definitions:
            if d == 'Z':
                args.append(<bint>va_arg(j_args, bool_type))
            elif d == 'B':
                args.append(<char>va_arg(j_args, char_type))
            elif d == 'C':
                args.append(<char>va_arg(j_args, byte_type))
            elif d == 'S':
                args.append(<short>va_arg(j_args, short_type))
            elif d == 'I':
                args.append(<int>va_arg(j_args, int_type))
            elif d == 'J':
                args.append(<long>va_arg(j_args, long_type))
            elif d == 'F':
                args.append(<float>va_arg(j_args, float_type))
            elif d == 'D':
                args.append(<double>va_arg(j_args, double_type))
            else: # == L, java object
                l = <void*>va_arg(j_args, pointer_type)
                args.append(convert_jobject_to_python(self.j_env, d, l))

        va_end(j_args)

        return self.callback(*args)


    cdef int call_int(self, ...):
        cdef va_list j_args
        cdef int n
        cdef void* l

        args = []

        va_start(j_args, <void*>self)

        for d in self.definitions:
            if d == 'Z':
                args.append(<bint>va_arg(j_args, bool_type))
            elif d == 'B':
                args.append(<char>va_arg(j_args, char_type))
            elif d == 'C':
                args.append(<char>va_arg(j_args, byte_type))
            elif d == 'S':
                args.append(<short>va_arg(j_args, short_type))
            elif d == 'I':
                args.append(<int>va_arg(j_args, int_type))
            elif d == 'J':
                args.append(<long>va_arg(j_args, long_type))
            elif d == 'F':
                args.append(<float>va_arg(j_args, float_type))
            elif d == 'D':
                args.append(<double>va_arg(j_args, double_type))
            else: # == L, java object
                l = <void*>va_arg(j_args, pointer_type)
                args.append(convert_jobject_to_python(self.j_env, d, l))

        va_end(j_args)

        return self.callback(*args)


    cdef long call_long(self, ...):
        cdef va_list j_args
        cdef int n
        cdef void* l

        args = []

        va_start(j_args, <void*>self)

        for d in self.definitions:
            if d == 'Z':
                args.append(<bint>va_arg(j_args, bool_type))
            elif d == 'B':
                args.append(<char>va_arg(j_args, char_type))
            elif d == 'C':
                args.append(<char>va_arg(j_args, byte_type))
            elif d == 'S':
                args.append(<short>va_arg(j_args, short_type))
            elif d == 'I':
                args.append(<int>va_arg(j_args, int_type))
            elif d == 'J':
                args.append(<long>va_arg(j_args, long_type))
            elif d == 'F':
                args.append(<float>va_arg(j_args, float_type))
            elif d == 'D':
                args.append(<double>va_arg(j_args, double_type))
            else: # == L, java object
                l = <void*>va_arg(j_args, pointer_type)
                args.append(convert_jobject_to_python(self.j_env, d, l))

        va_end(j_args)

        return self.callback(*args)


    cdef float call_float(self, ...):
        cdef va_list j_args
        cdef int n
        cdef void* l

        args = []

        va_start(j_args, <void*>self)

        for d in self.definitions:
            if d == 'Z':
                args.append(<bint>va_arg(j_args, bool_type))
            elif d == 'B':
                args.append(<char>va_arg(j_args, char_type))
            elif d == 'C':
                args.append(<char>va_arg(j_args, byte_type))
            elif d == 'S':
                args.append(<short>va_arg(j_args, short_type))
            elif d == 'I':
                args.append(<int>va_arg(j_args, int_type))
            elif d == 'J':
                args.append(<long>va_arg(j_args, long_type))
            elif d == 'F':
                args.append(<float>va_arg(j_args, float_type))
            elif d == 'D':
                args.append(<double>va_arg(j_args, double_type))
            else: # == L, java object
                l = <void*>va_arg(j_args, pointer_type)
                args.append(convert_jobject_to_python(self.j_env, d, l))

        va_end(j_args)

        return self.callback(*args)

    cdef double call_double(self, ...):
        cdef va_list j_args
        cdef int n
        cdef void* l

        args = []

        va_start(j_args, <void*>self)

        for d in self.definitions:
            if d == 'Z':
                args.append(<bint>va_arg(j_args, bool_type))
            elif d == 'B':
                args.append(<char>va_arg(j_args, char_type))
            elif d == 'C':
                args.append(<char>va_arg(j_args, byte_type))
            elif d == 'S':
                args.append(<short>va_arg(j_args, short_type))
            elif d == 'I':
                args.append(<int>va_arg(j_args, int_type))
            elif d == 'J':
                args.append(<long>va_arg(j_args, long_type))
            elif d == 'F':
                args.append(<float>va_arg(j_args, float_type))
            elif d == 'D':
                args.append(<double>va_arg(j_args, double_type))
            else: # == L, java object
                l = <void*>va_arg(j_args, pointer_type)
                args.append(convert_jobject_to_python(self.j_env, d, l))

        va_end(j_args)

        return self.callback(*args)

    #cdef jobject call_obj(self, ...):
    #    cdef va_list j_args
    #    cdef int n
    #    cdef void* l

    #    args = []

    #    va_start(j_args, <void*>self)

    #    for d in self.definitions:
    #        if d == 'Z':
    #            args.append(<bint>va_arg(j_args, bool_type))
    #        elif d == 'B':
    #            args.append(<char>va_arg(j_args, char_type))
    #        elif d == 'C':
    #            args.append(<char>va_arg(j_args, byte_type))
    #        elif d == 'S':
    #            args.append(<short>va_arg(j_args, short_type))
    #        elif d == 'I':
    #            args.append(<int>va_arg(j_args, int_type))
    #        elif d == 'J':
    #            args.append(<long>va_arg(j_args, long_type))
    #        elif d == 'F':
    #            args.append(<float>va_arg(j_args, float_type))
    #        elif d == 'D':
    #            args.append(<double>va_arg(j_args, double_type))
    #        else: # == L, java object
    #            l = <void*>va_arg(j_args, pointer_type)
    #            args.append(convert_jobject_to_python(self.j_env, d, l))

    #    va_end(j_args)

    #    return self.callback(*args)
