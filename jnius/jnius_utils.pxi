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


import functools
import traceback
class java_implementation(object):
    def __init__(self, signature, name=None):
        super(java_implementation, self).__init__()
        self.signature = signature
        self.name = name

    def __get__(self, instance, instancetype):
        return functools.partial(self.__call__, instance)

    def __call__(self, f):
        f.__javasignature__ = self.signature
        f.__javaname__ = self.name
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
            self.__javamethods__[(attr.__javaname__ or x, signature)] = attr

    def invoke(self, method, *args):
        try:
            ret = self._invoke(method, *args)
            return ret
        except Exception as e:
            traceback.print_exc(e)
            return None

    def _invoke(self, method, *args):
        from .reflect import get_signature
        #print 'PythonJavaClass.invoke() called with args:', args
        # search the java method

        ret_signature = get_signature(method.getReturnType())
        args_signature = tuple([get_signature(x) for x in method.getParameterTypes()])
        method_name = method.getName()

        key = (method_name, (ret_signature, args_signature))

        py_method = self.__javamethods__.get(key, None)
        if not py_method:
            print
            print '===== Python/java method missing ======'
            print 'Python class:', self
            print 'Java method name:', method_name
            print 'Signature: ({}){}'.format(''.join(args_signature), ret_signature)
            print '======================================='
            print
            raise NotImplemented('The method {} is not implemented'.format(key))

        return py_method(*args)

cdef jobject invoke0(JNIEnv *j_env, jobject j_this, jobject j_proxy, jobject
        j_method, jobjectArray args) except *:
    from .reflect import get_signature

    # get the python object
    cdef jfieldID ptrField = j_env[0].GetFieldID(j_env,
        j_env[0].GetObjectClass(j_env, j_this), "ptr", "J")
    cdef jlong jptr = j_env[0].GetLongField(j_env, j_this, ptrField)
    cdef object py_obj = <object>jptr

    # extract the method information
    # FIXME: only one call is not working sometimes ????+??????O?O??O?O
    method = convert_jobject_to_python(j_env, b'Ljava/lang/reflect/Method;', j_method)
    method = convert_jobject_to_python(j_env, b'Ljava/lang/reflect/Method;', j_method)
    ret_signature = get_signature(method.getReturnType())
    args_signature = [get_signature(x) for x in method.getParameterTypes()]

    # convert java argument to python object
    # native java type are given with java.lang.*, even if the signature say
    # it's a native type.
    cdef jobject j_arg
    py_args = []
    convert_signature = {
        'Z': 'Ljava/lang/Boolean;',
        'B': 'Ljava/lang/Byte;',
        'C': 'Ljava/lang/Character;',
        'S': 'Ljava/lang/Short;',
        'I': 'Ljava/lang/Integer;',
        'J': 'Ljava/lang/Long;',
        'F': 'Ljava/lang/Float;',
        'D': 'Ljava/lang/Double;'}

    for index, arg_signature in enumerate(args_signature):
        print 'convert signature', index, arg_signature
        arg_signature = convert_signature.get(arg_signature, arg_signature)
        j_arg = j_env[0].GetObjectArrayElement(j_env, args, index)
        py_arg = convert_jobject_to_python(j_env, arg_signature, j_arg)
        py_args.append(py_arg)

    # really invoke the python method
    print '- python invoke', method.getName(), py_args
    ret = py_obj.invoke(method, *py_args)

    # convert back to the return type
    # use the populate_args(), but in the reverse way :)
    t = ret_signature[:1]

    # did python returned a "native" type ?
    jtype = None

    if ret_signature == 'Ljava/lang/Object;':
        # generic object, try to manually convert it
        tp = type(ret)
        if tp == int:
            jtype = 'J'
        elif tp == float:
            jtype = 'D'
        elif tp == bool:
            jtype = 'Z'
    elif len(ret_signature) == 1:
        jtype = ret_signature

    cdef jobject jret

    try:
        jret = convert_python_to_jobject(j_env, jtype or ret_signature, ret)
        return jret
    except Exception as e:
        traceback.print_exc(e)



# now we need to create a proxy and pass it an invocation handler

cdef create_proxy_instance(JNIEnv *j_env, py_obj, j_interfaces):
    from .reflect import autoclass
    Proxy = autoclass('java.lang.reflect.Proxy')
    NativeInvocationHandler = autoclass('jnius.NativeInvocationHandler')
    ClassLoader = autoclass('java.lang.ClassLoader')

    # convert strings to Class
    j_interfaces = [find_javaclass(x) for x in j_interfaces]

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
        __javainterfaces__ = [
            #'java/util/Iterator',
            'java/util/ListIterator',]

        def __init__(self, collection, index=0):
            super(TestImplemIterator, self).__init__()
            self.collection = collection
            self.index = index

        @java_implementation('()Z')
        def hasNext(self):
            return self.index < len(self.collection.data)

        @java_implementation('()Ljava/lang/Object;')
        def next(self):
            obj = self.collection.data[self.index]
            self.index += 1
            return obj

        @java_implementation('()Z')
        def hasPrevious(self):
            return self.index >= 0

        @java_implementation('()Ljava/lang/Object;')
        def previous(self):
            self.index -= 1
            obj = self.collection.data[self.index]
            print "previous called", obj
            return obj

        @java_implementation('()I')
        def previousIndex(self):
            return self.index - 1

        @java_implementation('()Ljava/lang/String;')
        def toString(self):
            return repr(self)

    class TestImplem(PythonJavaClass):
        __javainterfaces__ = ['java/util/List']

        def __init__(self, *args):
            super(TestImplem, self).__init__()
            self.data = list(args)

        @java_implementation('()Ljava/util/Iterator;')
        def iterator(self):
            it = TestImplemIterator(self)
            return it

        @java_implementation('()Ljava/lang/String;')
        def toString(self):
            return repr(self)

        @java_implementation('()I')
        def size(self):
            return len(self.data)

        @java_implementation('(I)Ljava/lang/Object;')
        def get(self, index):
            return self.data[index]

        @java_implementation('(ILjava/lang/Object;)Ljava/lang/Object;')
        def set(self, index, obj):
            old_object = self.data[index]
            self.data[index] = obj
            return old_object

        @java_implementation('()[Ljava/lang/Object;')
        def toArray(self):
            return self.data

        @java_implementation('()Ljava/util/ListIterator;')
        def listIterator(self):
            it = TestImplemIterator(self)
            return it

        @java_implementation('(I)Ljava/util/ListIterator;',
                name='ListIterator')
        def listIteratorI(self, index):
            it = TestImplemIterator(self, index)
            return it


    print '2: instanciate the class, with some data'
    a = TestImplem(*range(10))
    print a
    print dir(a)

    print '3: Do cast to a collection'
    a2 = cast('java/util/Collection', a.j_self)

    print '4: Try few method on the collection'
    Collections = autoclass('java.util.Collections')
    #print Collections.enumeration(a)
    #print Collections.enumeration(a)
    ret = Collections.max(a)
    print 'MAX returned', ret

    # the first one of the following methods will work, witchever it is
    # the next ones will fail
    print "reverse"
    print Collections.reverse(a)
    print a.data

    print "reverse"
    print Collections.reverse(a)
    print a.data

    print "before swap"
    print Collections.swap(a, 2, 3)
    print "after swap"
    print a.data

    print "rotate"
    print Collections.rotate(a, 5)
    print a.data

    print 'Order of data before shuffle()', a.data
    print Collections.shuffle(a)
    print 'Order of data after shuffle()', a.data


    # XXX We have issues for methosd with multiple signature
    #print '-> Collections.max(a)'
    #print Collections.max(a2)
    #print '-> Collections.max(a)'
    #print Collections.max(a2)
    #print '-> Collections.shuffle(a)'
    #print Collections.shuffle(a2)
