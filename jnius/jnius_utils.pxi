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
                return 10

            if not isinstance(arg, tuple) and not isinstance(arg, list):
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

'''
cdef class GenericNativeWrapper(object):
    """
    This class is to be used to register python method as methods of
    JavaObjects using RegisterNatives
    """
    cdef JNIEnv* j_env
    cdef args

    def __cinit__(self, j_env, name, definition, callback):
        self.j_env = NULL
        self.j_nm = JNINativeMethod

    def __init__(self, j_env, name, definition, callback):
        self.callback = callback
        self.definitions = parse_definition(definition)
        self.nm.name = name
        self.nm.signature = definitions
        self.fnPtr = {
           'V': self.call_void,
           'L': self.call_obj,
           'D': self.call_double,
           'F': self.call_float,
           'J': self.call_long,
           'I': self.call_int,
           'S': self.call_short,
           'C': self.call_char,
           'B': self.call_byte,
           'Z': self.call_bool}[self.definitions[0]]

    cdef void call_void(self, ...):
        cdef va_list j_args
        cdef int n
        cdef void* l

        args = []

        va_start(j_args, <void*>self)

        for d in self.definitions[1]:
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

    cdef bint call_boot(self, ...):
        cdef va_list j_args
        cdef int n
        cdef void* l

        args = []

        va_start(j_args, <void*>self)

        for d in self.definitions[1]:
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

        for d in self.definitions[1]:
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

        for d in self.definitions[1]:
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

        for d in self.definitions[1]:
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

        for d in self.definitions[1]:
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

        for d in self.definitions[1]:
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

        for d in self.definitions[1]:
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

        for d in self.definitions[1]:
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

    #    for d in self.definitions[1]:
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
'''

import functools
class java_implementation(object):
    def __init__(self, signature):
        super(java_implementation, self).__init__()
        self.signature = signature

    def __get__(self, instance, instancetype):
        return functools.partial(self.__call__, instance)

    def __call__(self, f):
        f.__javasignature__ = self.signature
        return f

cdef class PythonJavaClass(object):
    '''
    base class to create a java class from python
    '''
    cdef JNIEnv *j_env
    cdef jclass j_cls
    cdef public object j_self

    def __cinit__(self, *args):
        self.j_env = get_jnienv()
        self.j_cls = NULL
        self.j_self = None

    def __init__(self, *args, **kwargs):
        self.j_self = create_proxy_instance(self.j_env, self,
            self.__javainterfaces__)

        # discover all the java method implementated
        self.__javamethods__ = {}
        for x in dir(self):
            attr = getattr(self, x)
            if not callable(attr):
                continue
            if not hasattr(attr, '__javasignature__'):
                continue
            signature = parse_definition(attr.__javasignature__)
            self.__javamethods__[(x, signature)] = attr

    def invoke(self, method, *args):
        from .reflect import get_signature
        print 'PythonJavaClass.invoke() called with args:', args
        # search the java method

        ret_signature = get_signature(method.getReturnType())
        args_signature = tuple([get_signature(x) for x in method.getParameterTypes()])
        method_name = method.getName()

        key = (method_name, (ret_signature, args_signature))
        print 'PythonJavaClass.invoke() want to invoke', key

        py_method = self.__javamethods__.get(key, None)
        if not py_method:
            raise NotImplemented('The method {0} is not implemented'.format(key))

        return py_method(*args)

cdef jobject invoke0(JNIEnv *j_env, jobject j_this, jobject j_proxy, jobject j_method, jobjectArray args):
    from .reflect import get_signature

    # get the python object
    cdef jfieldID ptrField = j_env[0].GetFieldID(j_env,
        j_env[0].GetObjectClass(j_env, j_this), "ptr", "J")
    cdef jlong jptr = j_env[0].GetLongField(j_env, j_this, ptrField)
    cdef object py_obj = <object>jptr

    # extract the method information
    # TODO: cache ?
    method = convert_jobject_to_python(j_env, b'Ljava/lang/reflect/Method;', j_method)
    ret_signature = get_signature(method.getReturnType())
    args_signature = ''.join([get_signature(x) for x in method.getParameterTypes()])

    # XX implement java array conversion
    py_args = []
    ret = py_obj.invoke(method, *py_args)

    # convert back to the return type
    # use the populate_args(), but in the reverse way :)
    cdef jvalue j_ret[1]
    populate_args(j_env, (ret_signature, ), <jvalue *>j_ret, [ret])
    return <jobject>j_ret


# now we need to create a proxy and pass it an invocation handler

cdef create_proxy_instance(JNIEnv *j_env, py_obj, j_interfaces):
    from .reflect import autoclass
    Proxy = autoclass('java.lang.reflect.Proxy')
    NativeInvocationHandler = autoclass('jnius.NativeInvocationHandler')
    ClassLoader = autoclass('java.lang.ClassLoader')

    # convert strings to Class
    j_interfaces = [find_javaclass(x) for x in j_interfaces]
    print 'create_proxy_instance', j_interfaces

    cdef JavaClass nih = NativeInvocationHandler(<long><void *>py_obj)
    cdef JNINativeMethod invoke_methods[1]
    invoke_methods[0].name = 'invoke0'
    invoke_methods[0].signature = '(Ljava/lang/Object;Ljava/lang/reflect/Method;[Ljava/lang/Object;)Ljava/lang/Object;'
    invoke_methods[0].fnPtr = <void *>&invoke0
    j_env[0].RegisterNatives(j_env, nih.j_cls, <JNINativeMethod *>invoke_methods, 1)

    cdef JavaClass j_obj = Proxy.newProxyInstance(
            ClassLoader.getSystemClassLoader(), j_interfaces, nih)

    #for name, definition, method in py_obj.j_methods:
    #    nw = GenericNativeWrapper(j_env, name, definition, method)
    #    j_env.RegisterNatives(j_env[0], cls, nw.nm, 1)

    # adds it to the invocationhandler

    # create the proxy and pass it the invocation handler
    return j_obj

def test():
    from .reflect import autoclass

    print '1: declare a TestImplem that implement Collection'
    class TestImplemIterator(PythonJavaClass):
        __javainterfaces__ = ['java/util/Iterator']

        def __init__(self, collection):
            super(TestImplemIterator, self).__init__()
            self.collection = collection
            self.index = 0

        @java_implementation('()B')
        def hasNext(self):
            return self.index < len(self.collection.data)

        @java_implementation('()Ljava/lang/Object;')
        def next(self):
            obj = self.collection.data[self.index]
            self.index += 1
            return obj


    class TestImplem(PythonJavaClass):
        __javainterfaces__ = ['java/util/Collection']

        def __init__(self, *args):
            super(TestImplem, self).__init__()
            self.data = args

        @java_implementation('()Ljava/util/Iterator;')
        def iterator(self):
            it = TestImplemIterator(self)
            print 'iterator called, and returned', it
            return it

    print '2: instanciate the class, with some data'
    a = TestImplem(129387, 'aoesrch', 987, 'aoenth')
    print a
    print dir(a)

    print '3: Do cast to a collection'
    a2 = cast('java/util/Collection', a.j_self)

    print '4: Try few method on the collection'
    Collections = autoclass('java.util.Collections')
    print Collections.enumeration(a)
    #print Collections.enumeration(a)
    print Collections.max(a)


    # XXX We have issues for methosd with multiple signature
    #print '-> Collections.max(a)'
    #print Collections.max(a2)
    #print '-> Collections.max(a)'
    #print Collections.max(a2)
    #print '-> Collections.shuffle(a)'
    #print Collections.shuffle(a2)
