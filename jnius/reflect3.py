from jnius import JavaClass, MetaJavaClass, JavaMethod, JavaStaticMethod


class Class(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = 'java/lang/Class'

    forName = JavaStaticMethod('(Ljava/lang/String;)Ljava/lang/Class;')
    getConstructors = JavaMethod('()[Ljava/lang/reflect/Constructor;')
    getMethods = JavaMethod('()[Ljava/lang/reflect/Method;')
    getFields = JavaMethod('()[Ljava/lang/reflect/Field;')
    getDeclaredMethods = JavaMethod('()[Ljava/lang/reflect/Method;')
    getDeclaredFields = JavaMethod('()[Ljava/lang/reflect/Field;')
    getName = JavaMethod('()Ljava/lang/String;')


class Object(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = 'java/lang/Object'

    getClass = JavaMethod('()Ljava/lang/Class;')


class Modifier(JavaClass, metaclass=MetaJavaClass):
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


class Method(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = 'java/lang/reflect/Method'

    getName = JavaMethod('()Ljava/lang/String;')
    toString = JavaMethod('()Ljava/lang/String;')
    getParameterTypes = JavaMethod('()[Ljava/lang/Class;')
    getReturnType = JavaMethod('()Ljava/lang/Class;')
    getModifiers = JavaMethod('()I')
    isVarArgs = JavaMethod('()Z')


class Field(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = 'java/lang/reflect/Field'

    getName = JavaMethod('()Ljava/lang/String;')
    toString = JavaMethod('()Ljava/lang/String;')
    getType = JavaMethod('()Ljava/lang/Class;')
    getModifiers = JavaMethod('()I')


class Constructor(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = 'java/lang/reflect/Constructor'

    toString = JavaMethod('()Ljava/lang/String;')
    getParameterTypes = JavaMethod('()[Ljava/lang/Class;')
    getModifiers = JavaMethod('()I')
    isVarArgs = JavaMethod('()Z')
