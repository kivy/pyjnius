from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
__all__ = ('autoclass', 'ensureclass', 'protocol_map')
from six import with_metaclass
import logging

from .jnius import (
    JavaClass, MetaJavaClass, JavaMethod, JavaStaticMethod,
    JavaField, JavaStaticField, JavaMultipleMethod, find_javaclass,
    JavaException
)

log = logging.getLogger(__name__)
from collections import defaultdict


class Class(with_metaclass(MetaJavaClass, JavaClass)):
    __javaclass__ = 'java/lang/Class'

    desiredAssertionStatus = JavaMethod('()Z')
    forName = JavaMultipleMethod([
        ('(Ljava/lang/String,Z,Ljava/lang/ClassLoader;)Ljava/langClass;', True, False),
        ('(Ljava/lang/String;)Ljava/lang/Class;', True, False), ])
    getClassLoader = JavaMethod('()Ljava/lang/ClassLoader;')
    getClasses = JavaMethod('()[Ljava/lang/Class;')
    getComponentType = JavaMethod('()Ljava/lang/Class;')
    getConstructor = JavaMethod('([Ljava/lang/Class;)Ljava/lang/reflect/Constructor;')
    getConstructors = JavaMethod('()[Ljava/lang/reflect/Constructor;')
    getDeclaredClasses = JavaMethod('()[Ljava/lang/Class;')
    getDeclaredConstructor = JavaMethod('([Ljava/lang/Class;)Ljava/lang/reflect/Constructor;')
    getDeclaredConstructors = JavaMethod('()[Ljava/lang/reflect/Constructor;')
    getDeclaredField = JavaMethod('(Ljava/lang/String;)Ljava/lang/reflect/Field;')
    getDeclaredFields = JavaMethod('()[Ljava/lang/reflect/Field;')
    getDeclaredMethod = JavaMethod('(Ljava/lang/String,[Ljava/lang/Class;)Ljava/lang/reflect/Method;')
    getDeclaredMethods = JavaMethod('()[Ljava/lang/reflect/Method;')
    getDeclaringClass = JavaMethod('()Ljava/lang/Class;')
    getField = JavaMethod('(Ljava/lang/String;)Ljava/lang/reflect/Field;')
    getFields = JavaMethod('()[Ljava/lang/reflect/Field;')
    getInterfaces = JavaMethod('()[Ljava/lang/Class;')
    getMethod = JavaMethod('(Ljava/lang/String,[Ljava/lang/Class;)Ljava/lang/reflect/Method;')
    getMethods = JavaMethod('()[Ljava/lang/reflect/Method;')
    getModifiers = JavaMethod('()[I')
    getName = JavaMethod('()Ljava/lang/String;')
    getPackage = JavaMethod('()Ljava/lang/Package;')
    getProtectionDomain = JavaMethod('()Ljava/security/ProtectionDomain;')
    getResource = JavaMethod('(Ljava/lang/String;)Ljava/net/URL;')
    getResourceAsStream = JavaMethod('(Ljava/lang/String;)Ljava/io/InputStream;')
    getSigners = JavaMethod('()[Ljava/lang/Object;')
    getSuperclass = JavaMethod('()Ljava/lang/Class;')
    isArray = JavaMethod('()Z')
    isAssignableFrom = JavaMethod('(Ljava/lang/Class;)Z')
    isInstance = JavaMethod('(Ljava/lang/Object;)Z')
    isInterface = JavaMethod('()Z')
    isPrimitive = JavaMethod('()Z')
    newInstance = JavaMethod('()Ljava/lang/Object;')
    toString = JavaMethod('()Ljava/lang/String;')

    def __str__(self):
        return (
            '%s: [%s]' if self.isArray() else '%s: %s'
        ) % (
            'Interface' if self.isInterface() else
            'Primitive' if self.isPrimitive() else
            'Class',
            self.getName()
        )

    def __repr__(self):
        return '<%s at 0x%x>' % (self, id(self))


class Object(with_metaclass(MetaJavaClass, JavaClass)):
    __javaclass__ = 'java/lang/Object'

    getClass = JavaMethod('()Ljava/lang/Class;')
    hashCode = JavaMethod('()I')


class Modifier(with_metaclass(MetaJavaClass, JavaClass)):
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


class Method(with_metaclass(MetaJavaClass, JavaClass)):
    __javaclass__ = 'java/lang/reflect/Method'

    getName = JavaMethod('()Ljava/lang/String;')
    toString = JavaMethod('()Ljava/lang/String;')
    getParameterTypes = JavaMethod('()[Ljava/lang/Class;')
    getReturnType = JavaMethod('()Ljava/lang/Class;')
    getModifiers = JavaMethod('()I')
    isVarArgs = JavaMethod('()Z')


class Field(with_metaclass(MetaJavaClass, JavaClass)):
    __javaclass__ = 'java/lang/reflect/Field'

    getName = JavaMethod('()Ljava/lang/String;')
    toString = JavaMethod('()Ljava/lang/String;')
    getType = JavaMethod('()Ljava/lang/Class;')
    getModifiers = JavaMethod('()I')


class Constructor(with_metaclass(MetaJavaClass, JavaClass)):
    __javaclass__ = 'java/lang/reflect/Constructor'

    toString = JavaMethod('()Ljava/lang/String;')
    getParameterTypes = JavaMethod('()[Ljava/lang/Class;')
    getModifiers = JavaMethod('()I')
    isVarArgs = JavaMethod('()Z')


def get_signature(cls_tp):
    tp = cls_tp.getName()
    if tp[0] == '[':
        return tp.replace('.', '/')
    signatures = {
        'void': 'V', 'boolean': 'Z', 'byte': 'B',
        'char': 'C', 'short': 'S', 'int': 'I',
        'long': 'J', 'float': 'F', 'double': 'D'}
    ret = signatures.get(tp)
    if ret:
        return ret
    # don't do it in recursive way for the moment,
    # error on the JNI/android: JNI ERROR (app bug): local reference table
    # overflow (max=512)

    # ensureclass(tp)
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


def lower_name(s):
    return s[:1].lower() + s[1:] if s else ''


def bean_getter(s):
    return (s.startswith('get') and len(s) > 3 and s[3].isupper()) or (s.startswith('is') and len(s) > 2 and s[2].isupper())


def log_method(method, name, signature):
    mods = method.getModifiers()
    log.debug(
        '\nmeth: %s\n'
        '  sig: %s\n'
        '  Public %s\n'
        '  Private %s\n'
        '  Protected %s\n'
        '  Static %s\n'
        '  Final %s\n'
        '  Synchronized %s\n'
        '  Volatile %s\n'
        '  Transient %s\n'
        '  Native %s\n'
        '  Interface %s\n'
        '  Abstract %s\n'
        '  Strict %s\n',
        name,
        signature,
        Modifier.isPublic(mods),
        Modifier.isPrivate(mods),
        Modifier.isProtected(mods),
        Modifier.isStatic(mods),
        Modifier.isFinal(mods),
        Modifier.isSynchronized(mods),
        Modifier.isVolatile(mods),
        Modifier.isTransient(mods),
        Modifier.isNative(mods),
        Modifier.isInterface(mods),
        Modifier.isAbstract(mods),
        Modifier.isStrict(mods)
    )

def identify_hierarchy(cls, level, concrete=True):
    supercls = cls.getSuperclass()
    if supercls is not None:
         for sup, lvl in identify_hierarchy(supercls, level + 1, concrete=concrete):
             yield sup, lvl # we could use yield from when we drop python2
    interfaces = cls.getInterfaces()
    for interface in interfaces or []:
        for sup, lvl in identify_hierarchy(interface, level + 1, concrete=concrete):
            yield sup, lvl
    # all object extends Object, so if this top interface in a hierarchy, yield Object
    if not concrete and cls.isInterface() and not interfaces:
        yield find_javaclass('java.lang.Object'), level +1
    yield cls, level


def autoclass(clsname, include_protected=False, include_private=False):
    jniname = clsname.replace('.', '/')
    cls = MetaJavaClass.get_javaclass(jniname)
    if cls:
        return cls

    classDict = {}

    # c = Class.forName(clsname)
    c = find_javaclass(clsname)
    if c is None:
        raise Exception('Java class {0} not found'.format(c))
        return None

    constructors = []
    for constructor in c.getConstructors():
        sig = '({0})V'.format(
            ''.join([get_signature(x) for x in constructor.getParameterTypes()]))
        constructors.append((sig, constructor.isVarArgs()))
    classDict['__javaconstructor__'] = constructors

    class_hierachy = list(identify_hierarchy(c, 0, not c.isInterface()))

    log.debug("autoclass(%s) intf %r hierarchy is %s" % (clsname,c.isInterface(),str(class_hierachy)))
    cls_done=set()

    cls_methods = defaultdict(list)
    cls_fields = defaultdict(list)

    # we now walk the hierarchy, from top of the tree, identifying methods
    # hopefully we start at java.lang.Object 
    for cls, level in class_hierachy:
        # dont analyse a given class more than once.
        # many interfaces can lead to java.lang.Object 
        if cls in cls_done:
            continue
        cls_done.add(cls)
        # as we are walking the entire hierarchy, we only need getDeclaredMethods()
        # to get what is in this class; other parts of the hierarchy will be found
        # in those respective classes.
        methods = cls.getDeclaredMethods()
        methods_name = [x.getName() for x in methods]
        # collect all methods declared by this class of the hierarchy for later traversal
        for index, method in enumerate(methods):
            method_modifier = method.getModifiers()
            if Modifier.isProtected(method_modifier) and not include_protected:
                continue
            if Modifier.isPrivate(method_modifier) and not include_private:
                continue
            name = methods_name[index]
            cls_methods[name].append((cls, method, level))
    
        fields = cls.getDeclaredFields()
        for field in fields:
            field_name = field.getName()
            cls_fields[field_name].append((cls, field, level))

    # having collated the methods, identify if there are any with the same name
    for name in cls_methods:
        if len(cls_methods[name]) == 1:
            # uniquely named method
            owningCls, method, level = cls_methods[name][0]
            static = Modifier.isStatic(method.getModifiers())
            varargs = method.isVarArgs()
            sig = '({0}){1}'.format(
                ''.join([get_signature(x) for x in method.getParameterTypes()]),
                get_signature(method.getReturnType()))
            if log.level <= logging.DEBUG:
                log_method(method, name, sig)
            classDict[name] = (JavaStaticMethod if static else JavaMethod)(sig, varargs=varargs)
            if name != 'getClass' and bean_getter(name) and len(method.getParameterTypes()) == 0:
                lowername = lower_name(name[2 if name.startswith('is') else 3:])
                classDict[lowername] = (lambda n: property(lambda self: getattr(self, n)()))(name)
        else:
            # multiple signatures
            signatures = []
            log.debug("method %s has %d multiple signatures in hierarchy of cls %s" % (name, len(cls_methods[name]), c))

            paramsig_to_level=defaultdict(lambda: float('inf'))
            # we now identify if any have the same signature, as we will call the _lowest_ in the hierarchy,
            # as reflected in min level
            for owningCls, method, level in cls_methods[name]:
                param_sig = ''.join([get_signature(x) for x in method.getParameterTypes()])
                log.debug("\t owner %s level %d param_sig %s" % (str(owningCls), level, param_sig))
                if level < paramsig_to_level[param_sig]:
                    paramsig_to_level[param_sig] = level

            for owningCls, method, level in cls_methods[name]:
                param_sig = ''.join([get_signature(x) for x in method.getParameterTypes()])
                # only accept the parameter signature at the deepest level of hierarchy (i.e. min level)
                if level > paramsig_to_level[param_sig]:
                    log.debug("discarding %s name from %s at level %d" % (name, str(owningCls), level))
                    continue

                return_sig = get_signature(method.getReturnType())
                sig = '({0}){1}'.format(param_sig, return_sig)
                
                if log.level <= logging.DEBUG:
                    log_method(method, name, sig)
                signatures.append((sig, Modifier.isStatic(method.getModifiers()), method.isVarArgs()))

            log.debug("method selected %d multiple signatures of %s" % (len(signatures), str(signatures)))
            classDict[name] = JavaMultipleMethod(signatures)

    # check whether any classes in the hierarchy appear in the protocol_map
    for cls, _ in class_hierachy:
        cls_name = cls.getName()
        if cls_name in protocol_map:
            for pname, plambda in protocol_map[cls_name].items():
                classDict[pname] = plambda  

    for field_name in cls_fields:
        num_matches = len(cls_fields[field_name])
        print("field %s has %d matches in hierarchy of %s" % (field_name, num_matches, clsname))
        if num_matches == 1:
            # only one with this name exists
            owningCls, field, level = cls_fields[field_name][0]

            field_modifier = field.getModifiers()
            static = Modifier.isStatic(field_modifier)
            sig = get_signature(field.getType())
            if Modifier.isProtected(field_modifier) and not include_protected:
                continue
            if Modifier.isPrivate(field_modifier) and not include_private:
                continue
            cls = JavaStaticField if static else JavaField

            #append _ for a field if a method of the same name already exists
            py_field_name = field_name + "_" if field_name in classDict else field_name

            classDict[py_field_name] = cls(sig, j_name= field_name, j_class_name = owningCls.getName())
        else:
            # num_matches fields with the same name exist.
            for i, (owningCls, field, level) in enumerate(cls_fields[field_name]):
                #last occurrences gets <field_name>, one before gets super_<field_name> etc 
                py_field_name = ''.join(["super_"] * (num_matches-i-1)) + field_name
                field_modifier = field.getModifiers()
                static = Modifier.isStatic(field_modifier)
                sig = get_signature(field.getType())
                if Modifier.isProtected(field_modifier) and not include_protected:
                    continue
                if Modifier.isPrivate(field_modifier) and not include_private:
                    continue
                cls = JavaStaticField if static else JavaField

                #append _ for a field if a method of the same name already exists
                py_field_name = py_field_name + "_" if py_field_name in classDict else py_field_name
                print("resolved %s to %s" % (field_name, py_field_name))
                classDict[py_field_name] = cls(sig, j_name= field_name, j_class_name = owningCls.getName())

    classDict['__javaclass__'] = clsname.replace('.', '/')
    return MetaJavaClass.__new__(
        MetaJavaClass,
        clsname,
        (JavaClass, ),
        classDict)


## dunder method for List
def _getitem(self, index):
    try:
        return self.get(index)
    except JavaException as e:
        # initialize the subclass before getting the Class.forName
        # otherwise isInstance does not know of the subclass
        mock_exception_object = autoclass(e.classname)()
        if find_javaclass("java.lang.IndexOutOfBoundsException").isInstance(mock_exception_object):
            # python for...in iteration checks for end of list by waiting for IndexError
            raise IndexError()
        else:
            raise

# protocol_map is a user-accessible API for patching class instances with additional methods 
protocol_map = {
    'java.util.Collection' : {
        '__len__' : lambda self: self.size()
    },
    'java.util.List' : {
        '__getitem__' : _getitem        
    },
    # this also addresses java.io.Closeable
    'java.lang.AutoCloseable' : {
        '__enter__' : lambda self: self,
        '__exit__' : lambda self, type, value, traceback: self.close()
    }
}
