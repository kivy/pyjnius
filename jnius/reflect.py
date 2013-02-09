__all__ = ('autoclass', 'ensureclass')
import sys

from jnius import JavaClass, MetaJavaClass, JavaMethod, JavaStaticMethod, \
        JavaField, JavaStaticField, JavaMultipleMethod, find_javaclass
if sys.version_info < (3, 0):
    from .reflect2 import Class, Object, Modifier, Method, Field, Constructor
else:
    from .reflect3 import Class, Object, Modifier, Method, Field, Constructor


def get_signature(cls_tp):
    tp = cls_tp.getName()
    if tp[0] == '[':
        return tp.replace('.', '/')
    signatures = { 'void': 'V', 'boolean': 'Z', 'byte': 'B',
        'char': 'C', 'short': 'S', 'int': 'I',
        'long': 'J', 'float': 'F', 'double': 'D'}
    ret = signatures.get(tp)
    if ret:
        return ret
    # don't do it in recursive way for the moment,
    # error on the JNI/android: JNI ERROR (app bug): local reference table overflow (max=512)
    #
    #ensureclass(tp)
    return 'L{0};'.format(tp.replace('.', '/'))


registers = []

def ensureclass(clsname):
    if clsname in registers:
        return
    jniname = clsname.replace('.', '/')
    if MetaJavaClass.get_javaclass(jniname):
        return
    registers.append(clsname)
    autoclass(clsname)


def autoclass(clsname):
    jniname = clsname.replace('.', '/')
    cls = MetaJavaClass.get_javaclass(jniname)
    if cls:
        return cls

    clsname = str(clsname)
    classDict = {}

    #c = Class.forName(clsname)
    c = find_javaclass(clsname)
    if c is None:
        raise Exception('Java class {0} not found'.format(c))
        return None

    constructors = []
    for constructor in c.getConstructors():
        sig = '({0})V'.format(''.join(
            [get_signature(x) for x in constructor.getParameterTypes()]))
        constructors.append((sig, constructor.isVarArgs()))
    classDict['__javaconstructor__'] = constructors

    methods = c.getMethods()
    methods_name = [x.getName() for x in methods]
    for index, method in enumerate(methods):
        name = methods_name[index]
        if name in classDict:
            continue
        count = methods_name.count(name)

        # only one method available
        if count == 1:
            static = Modifier.isStatic(method.getModifiers())
            varargs = method.isVarArgs()
            sig = '({0}){1}'.format(
                ''.join([get_signature(x) for x in method.getParameterTypes()]),
                get_signature(method.getReturnType()))
            cls = JavaStaticMethod if static else JavaMethod
            classDict[name] = cls(sig, varargs=varargs)
            continue

        # multpile signatures
        signatures = []
        for index, subname in enumerate(methods_name):
            if subname != name:
                continue
            method = methods[index]
            sig = '({0}){1}'.format(
                ''.join([get_signature(x) for x in method.getParameterTypes()]),
                get_signature(method.getReturnType()))
            '''
            print 'm', name, sig, method.getModifiers()
            m = method.getModifiers()
            print 'Public', Modifier.isPublic(m)
            print 'Private', Modifier.isPrivate(m)
            print 'Protected', Modifier.isProtected(m)
            print 'Static', Modifier.isStatic(m)
            print 'Final', Modifier.isFinal(m)
            print 'Synchronized', Modifier.isSynchronized(m)
            print 'Volatile', Modifier.isVolatile(m)
            print 'Transient', Modifier.isTransient(m)
            print 'Native', Modifier.isNative(m)
            print 'Interface', Modifier.isInterface(m)
            print 'Abstract', Modifier.isAbstract(m)
            print 'Strict', Modifier.isStrict(m)
            '''
            signatures.append((sig, Modifier.isStatic(method.getModifiers()), method.isVarArgs()))

        classDict[name] = JavaMultipleMethod(signatures)

    for field in c.getFields():
        static = Modifier.isStatic(field.getModifiers())
        sig = get_signature(field.getType())
        cls = JavaStaticField if static else JavaField
        classDict[field.getName()] = cls(sig)

    classDict['__javaclass__'] = clsname.replace('.', '/')

    return MetaJavaClass.__new__(MetaJavaClass,
            clsname,#.replace('.', '_'),
            (JavaClass, ),
            classDict)
