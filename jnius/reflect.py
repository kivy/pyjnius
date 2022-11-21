from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from collections import defaultdict
import logging


from .jnius import (
    JavaClass, MetaJavaClass, JavaMethod, JavaStaticMethod,
    JavaField, JavaStaticField, JavaMultipleMethod, find_javaclass,
    JavaException, get_signature
)

__all__ = ('autoclass', 'ensureclass', 'protocol_map')

log = logging.getLogger('kivy').getChild(__name__)


class Class(JavaClass, metaclass=MetaJavaClass):
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


class Object(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = 'java/lang/Object'

    getClass = JavaMethod('()Ljava/lang/Class;')
    hashCode = JavaMethod('()I')


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
    isDefault = JavaMethod('()Z')


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


# NOTE: if you change the include_protected or include_private default values,
# you also must change the classparams default value in MetaJavaClass.__new__
# and MetaJavaClass.get_javaclass.
def autoclass(clsname, include_protected=True, include_private=True):
    jniname = clsname.replace('.', '/')
    cls = MetaJavaClass.get_javaclass(jniname, classparams=(include_protected, include_private))
    if cls:
        return cls

    classDict = {}
    cls_start_packagename = '.'.join(clsname.split('.')[:-1])

    # c = Class.forName(clsname)
    c = find_javaclass(clsname)
    if c is None:
        raise Exception('Java class {0} not found'.format(c))
        return None

    classDict['_class'] = c

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
    cls_fields = {}

    # we now walk the hierarchy, from top of the tree, identifying methods
    # hopefully we start at java.lang.Object 
    for cls, level in class_hierachy:
        # dont analyse a given class more than once.
        # many interfaces can lead to java.lang.Object
        if cls in cls_done:
            continue
        cls_packagename = '.'.join(cls.getName().split('.')[:-1])
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
            if not (Modifier.isPublic(method_modifier) or
                    Modifier.isProtected(method_modifier) or
                    Modifier.isPrivate(method_modifier)):
                if cls_start_packagename == cls_packagename and not include_protected:
                    continue
                if cls_start_packagename != cls_packagename and not include_private:
                    continue
            name = methods_name[index]
            cls_methods[name].append((cls, method, level))
    
        fields = cls.getDeclaredFields()
        for field in fields:
            field_name = field.getName()
            if field_name in cls_fields:
                if level < cls_fields[field_name][1]:
                    cls_fields[field_name] = (field, level, cls_packagename)
            else:
                cls_fields[field_name] = (field, level, cls_packagename)

    # the fields are analyzed before methods so that if a method and a field
    # have the same name, the field will take precedence in classDict.
    for field_name, (field, _, cls_packagename) in cls_fields.items():
        field_modifier = field.getModifiers()
        static = Modifier.isStatic(field_modifier)
        sig = get_signature(field.getType())
        if Modifier.isProtected(field_modifier) and not include_protected:
            continue
        if Modifier.isPrivate(field_modifier) and not include_private:
            continue
        if not (Modifier.isPublic(field_modifier) or
                Modifier.isProtected(field_modifier) or
                Modifier.isPrivate(field_modifier)):
            if cls_start_packagename == cls_packagename and not include_protected:
                continue
            if cls_start_packagename != cls_packagename and not include_private:
                continue
        cls = JavaStaticField if static else JavaField
        classDict[field_name] = cls(sig)

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
            if log.isEnabledFor(logging.DEBUG):
                log_method(method, name, sig)
            classDict[name] = (JavaStaticMethod if static else JavaMethod)(sig, varargs=varargs)
            # methods that fit the characteristics of a JavaBean's methods get turned into properties.
            # these added properties should not supercede any other methods or fields.
            if name != 'getClass' and bean_getter(name) and len(method.getParameterTypes()) == 0:
                lowername = lower_name(name[2 if name.startswith('is') else 3:])
                if lowername in classDict:
                    # don't add this to classDict if the property will replace a method or field.
                    continue
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

                if log.isEnabledFor(logging.DEBUG):
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

    classDict['__javaclass__'] = clsname.replace('.', '/')
    return MetaJavaClass.__new__(
        MetaJavaClass,
        clsname,
        (JavaClass, ),
        classDict,
        classparams=(include_protected, include_private))


def _getitem(self, index):
    ''' dunder method for List '''
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

def _map_getitem(self, k):
    ''' dunder method for java.util.Map '''
    rtr = self.get(k)
    if rtr is None:
        raise KeyError()
    return rtr


def _iterator_next(self):
    ''' dunder method for java.util.Iterator'''
    if not self.hasNext():
        raise StopIteration()

    return self.next()


# protocol_map is a user-accessible API for patching class instances with additional methods
protocol_map = {
    'java.util.Collection' : {
        '__len__' : lambda self: self.size(),
        '__contains__' : lambda self, item: self.contains(item),
        '__delitem__' : lambda self, item: self.remove(item)
    },
    'java.util.List' : {
        '__getitem__' : _getitem
    },
    'java.util.Map' : {
        '__setitem__' : lambda self, k, v : self.put(k,v),
        '__getitem__' : _map_getitem,
        '__delitem__' : lambda self, item: self.remove(item),
        '__len__' : lambda self: self.size(),
        '__contains__' : lambda self, item: self.containsKey(item),
        '__iter__' : lambda self: self.keySet().iterator()
    },
    'java.util.Iterator' : {
        '__iter__' : lambda self: self,
        '__next__' : _iterator_next,
    },
    'java.lang.Iterable' : {
        '__iter__' : lambda self: self.iterator(),
    },
    # this also addresses java.io.Closeable
    'java.lang.AutoCloseable' : {
        '__enter__' : lambda self: self,
        '__exit__' : lambda self, type, value, traceback: self.close()
    },
    'java.lang.Comparable' : {
        #__cmp__ is for Python 2 support
        '__cmp__' : lambda self, other: self.compareTo(other),
        '__eq__' : lambda self, other: self.equals(other),
        '__ne__' : lambda self, other: not self.equals(other),
        '__lt__' : lambda self, other: self.compareTo(other) < 0,
        '__gt__' : lambda self, other: self.compareTo(other) > 0,
        '__le__' : lambda self, other: self.compareTo(other) <= 0,
        '__ge__' : lambda self, other: self.compareTo(other) >= 0,
    }
}
