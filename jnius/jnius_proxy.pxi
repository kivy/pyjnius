class java_method(object):
    def __init__(self, signature, name=None):
        super(java_method, self).__init__()
        self.signature = signature
        self.name = name

    def __get__(self, instance, instancetype):
        return partial(self.__call__, instance)

    def __call__(self, f):
        f.__javasignature__ = self.signature
        f.__javaname__ = self.name
        return f


cdef class PythonJavaClass(object):
    '''
    Base class to create a java class from python
    '''
    cdef jclass j_cls
    cdef public object j_self

    def __cinit__(self, *args):
        self.j_cls = NULL
        self.j_self = None

    def __init__(self, *args, **kwargs):
        self._init_j_self_ptr()

    def _init_j_self_ptr(self):
        javacontext = 'system'
        if hasattr(self, '__javacontext__'):
            javacontext = self.__javacontext__
        self.j_self = create_proxy_instance(get_jnienv(), self,
            self.__javainterfaces__, javacontext)

        # discover all the java method implemented
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
        except Exception:
            traceback.print_exc()
            return None

    def _invoke(self, method, *args):
        from .reflect import get_signature
        # search the java method

        ret_signature = get_signature(method.getReturnType())
        args_signature = tuple([get_signature(x) for x in method.getParameterTypes()])
        method_name = method.getName()

        key = (method_name, (ret_signature, args_signature))

        py_method = self.__javamethods__.get(key, None)
        if not py_method:
            print(''.join([
                '\n===== Python/java method missing ======',
                '\nPython class:', repr(self),
                '\nJava method name:', method_name,
                '\nSignature: ({}){}'.format(''.join(args_signature), ret_signature),
                '\n=======================================\n']))
            raise NotImplementedError('The method {} is not implemented'.format(key))

        return py_method(*args)


cdef jobject py_invoke0(JNIEnv *j_env, jobject j_this, jobject j_proxy, jobject
        j_method, jobjectArray args) except * with gil:

    from .reflect import get_signature, Method
    cdef jfieldID ptrField
    cdef jlong jptr
    cdef object py_obj
    cdef JavaClass method
    cdef jobject j_arg

    # get the python object
    ptrField = j_env[0].GetFieldID(j_env,
        j_env[0].GetObjectClass(j_env, j_this), "ptr", "J")
    jptr = j_env[0].GetLongField(j_env, j_this, ptrField)
    py_obj = <object><void *>jptr

    # extract the method information
    method = Method(noinstance=True)
    method.instanciate_from(create_local_ref(j_env, j_method))
    ret_signature = get_signature(method.getReturnType())
    args_signature = [get_signature(x) for x in method.getParameterTypes()]

    # convert java argument to python object
    # native java type are given with java.lang.*, even if the signature say
    # it's a native type.
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
        arg_signature = convert_signature.get(arg_signature, arg_signature)
        j_arg = j_env[0].GetObjectArrayElement(j_env, args, index)
        py_arg = convert_jobject_to_python(j_env, arg_signature, j_arg)
        j_env[0].DeleteLocalRef(j_env, j_arg)
        py_args.append(py_arg)

    # really invoke the python method
    name = method.getName()
    ret = py_obj.invoke(method, *py_args)

    # convert back to the return type
    # use the populate_args(), but in the reverse way :)
    t = ret_signature[:1]

    # did python returned a "native" type ?
    jtype = None

    if ret_signature == 'Ljava/lang/Object;':
        # generic object, try to manually convert it
        tp = type(ret)
        if PY2 and tp == int:
            jtype = 'I'
        elif (PY2 and tp == long) or tp == int:
            jtype = 'J'
        elif tp == float:
            jtype = 'D'
        elif tp == bool:
            jtype = 'Z'
    elif len(ret_signature) == 1:
        jtype = ret_signature

    try:
        return convert_python_to_jobject(j_env, jtype or ret_signature, ret)
    except Exception:
        traceback.print_exc()


cdef jobject invoke0(JNIEnv *j_env, jobject j_this, jobject j_proxy, jobject
        j_method, jobjectArray args) with gil:
    try:
        return py_invoke0(j_env, j_this, j_proxy, j_method, args)
    except Exception:
        traceback.print_exc()
        return NULL

# now we need to create a proxy and pass it an invocation handler
cdef create_proxy_instance(JNIEnv *j_env, py_obj, j_interfaces, javacontext):
    from .reflect import autoclass
    Proxy = autoclass('java.lang.reflect.Proxy')
    NativeInvocationHandler = autoclass('org.jnius.NativeInvocationHandler')

    # convert strings to Class
    j_interfaces = [find_javaclass(x) for x in j_interfaces]

    cdef JavaClass nih = NativeInvocationHandler(<long long><void *>py_obj)
    cdef JNINativeMethod invoke_methods[1]
    invoke_methods[0].name = 'invoke0'
    invoke_methods[0].signature = '(Ljava/lang/Object;Ljava/lang/reflect/Method;[Ljava/lang/Object;)Ljava/lang/Object;'
    invoke_methods[0].fnPtr = <void *>&invoke0
    j_env[0].RegisterNatives(j_env, nih.j_cls, <JNINativeMethod *>invoke_methods, 1)

    # create the proxy and pass it the invocation handler
    cdef JavaClass j_obj
    if javacontext == 'app':
        Thread = autoclass('java.lang.Thread')
        classLoader = Thread.currentThread().getContextClassLoader()
        j_obj = Proxy.newProxyInstance(
                classLoader, j_interfaces, nih)

    elif javacontext == 'system':
        ClassLoader = autoclass('java.lang.ClassLoader')
        classLoader = ClassLoader.getSystemClassLoader()
        j_obj = Proxy.newProxyInstance(
                classLoader, j_interfaces, nih)

    else:
        raise Exception(
                'Invalid __javacontext__ {}, must be app or system.'.format(
                    javacontext))

    return j_obj
