from types import ClassType
from jnius import JavaClass, MetaJavaClass, JavaMethod, JavaStaticMethod, \
        JavaField, JavaStaticField

class Class(JavaClass):
    __metaclass__ = MetaJavaClass
    __javaclass__ = 'java/lang/Class'

    forName = JavaStaticMethod('(Ljava/lang/String;)Ljava/lang/Class;')
    getDeclaredMethods = JavaMethod('()[Ljava/lang/reflect/Method;')
    getDeclaredFields = JavaMethod('()[Ljava/lang/reflect/Field;')
    getName = JavaMethod('()Ljava/lang/String;')

class Object(JavaClass):
    __metaclass__ = MetaJavaClass
    __javaclass__ = 'java/lang/Object'

    getClass = JavaMethod('()Ljava/lang/Class;')

class Modifier(JavaClass):
    __metaclass__ = MetaJavaClass
    __javaclass__ = 'java/lang/reflect/Modifier'

    isAbstract = JavaStaticMethod('(I)Z')
    isFinal = JavaStaticMethod('(I)Z')
    isInterface = JavaStaticMethod('(I)Z')
    isNative = JavaStaticMethod('(I)Z')
    isPrivate = JavaStaticMethod('(I)Z')
    isProtected = JavaStaticMethod('(I)Z')
    isPublic = JavaStaticMethod('(I)Z')
    isStatic = JavaStaticMethod('(I)Z')
    isStrict = JavaStaticMethod('(I)Z')
    isSynchronized = JavaStaticMethod('(I)Z')
    isTransient = JavaStaticMethod('(I)Z')
    isVolatile = JavaStaticMethod('(I)Z')

class Method(JavaClass):
    __metaclass__ = MetaJavaClass
    __javaclass__ = 'java/lang/reflect/Method'

    getName = JavaMethod('()Ljava/lang/String;')
    toString = JavaMethod('()Ljava/lang/String;')
    getParameterTypes = JavaMethod('()[Ljava/lang/Class;')
    getReturnType = JavaMethod('()Ljava/lang/Class;')
    getModifiers = JavaMethod('()I')


class Field(JavaClass):
    __metaclass__ = MetaJavaClass
    __javaclass__ = 'java/lang/reflect/Field'

    getName = JavaMethod('()Ljava/lang/String;')
    toString = JavaMethod('()Ljava/lang/String;')
    getType = JavaMethod('()Ljava/lang/Class;')
    getModifiers = JavaMethod('()I')


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
    ensureclass(tp)
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
    if cls: return cls

    classDict = {}

    c = Class.forName(clsname)
    if c is None:
        raise Exception('Java class {0} not found'.format(c))
        return None

    for method in c.getDeclaredMethods():
        static = Modifier.isStatic(method.getModifiers())
        sig = '({0}){1}'.format(
            ''.join([get_signature(x) for x in method.getParameterTypes()]),
            get_signature(method.getReturnType()))
        cls = JavaStaticMethod if static else JavaMethod
        classDict[method.getName()] = cls(sig)

    for field in c.getDeclaredFields():
        static = Modifier.isStatic(field.getModifiers())
        sig = get_signature(field.getType())
        cls = JavaStaticField if static else JavaField
        classDict[field.getName()] = cls(sig)

    classDict['__javaclass__'] = clsname.replace('.', '/')

    return MetaJavaClass.__new__(MetaJavaClass,
            clsname,#.replace('.', '_'),
            (JavaClass, ),
            classDict)

