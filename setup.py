'''
Setup.py for creating a binary distribution.
'''

from __future__ import print_function
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension
try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess
import os
from os import environ
from os.path import dirname, join, exists, realpath
import sys
from platform import machine
from setup_sdist import SETUP_KWARGS

PY2 = sys.version_info < (3, 0, 0)


def getenv(key):
    '''Get value from environment and decode it.'''
    val = environ.get(key)
    if val is not None:
        if not PY2:
            try:
                return val.decode()
            except AttributeError:
                return val
    return val


FILES = [
    'jni.pxi',
    'jnius_compat.pxi',
    'jnius_conversion.pxi',
    'jnius_export_class.pxi',
    'jnius_export_func.pxi',
    'jnius_jvm_android.pxi',
    'jnius_jvm_desktop.pxi',
    'jnius_jvm_dlopen.pxi',
    'jnius_localref.pxi',
    'jnius.pyx',
    'jnius_utils.pxi',
]

LIBRARIES = []
LIBRARY_DIRS = []
LIB_LOCATION = None
EXTRA_LINK_ARGS = []
INCLUDE_DIRS = []
INSTALL_REQUIRES = ['six>=1.7.0']

# detect Python for android
PLATFORM = sys.platform
NDKPLATFORM = getenv('NDKPLATFORM')
if NDKPLATFORM is not None and getenv('LIBLINK'):
    PLATFORM = 'android'

# detect cython
try:
    from Cython.Distutils import build_ext
    INSTALL_REQUIRES.append('cython')
except ImportError:
    # pylint: disable=ungrouped-imports
    try:
        from setuptools.command.build_ext import build_ext
    except ImportError:
        from distutils.command.build_ext import build_ext
    if PLATFORM != 'android':
        print('\n\nYou need Cython to compile Pyjnius.\n\n')
        raise
    # On Android we expect to see 'c' files lying about.
    # and we go ahead with the 'desktop' file? Odd.
    FILES = [fn[:-3] + 'c' for fn in FILES if fn.endswith('pyx')]


def find_javac(possible_homes):
    '''Find javac in all possible locations.'''
    name = "javac.exe" if sys.platform == "win32" else "javac"
    for home in possible_homes:
        for javac in [join(home, name), join(home, 'bin', name)]:
            if exists(javac):
                return javac
    return name  # Fall back to "hope it's on the path"


def compile_native_invocation_handler(*possible_homes):
    '''Find javac and compile NativeInvocationHandler.java.'''
    javac = find_javac(possible_homes)
    subprocess.check_call([
        javac, '-target', '1.6', '-source', '1.6',
        join('jnius', 'src', 'org', 'jnius', 'NativeInvocationHandler.java')
    ])


if PLATFORM == 'android':
    # for android, we use SDL...
    LIBRARIES = ['sdl', 'log']
    LIBRARY_DIRS = ['libs/' + getenv('ARCH')]

elif PLATFORM == 'darwin':

    FRAMEWORK = subprocess.Popen(
        '/usr/libexec/java_home',
        stdout=subprocess.PIPE, shell=True).communicate()[0]

    if not PY2:
        FRAMEWORK = FRAMEWORK.decode('utf-8')

    FRAMEWORK = FRAMEWORK.strip()

    if not FRAMEWORK:
        raise Exception('You must install Java on your Mac OS X distro')

    if '1.6' in FRAMEWORK:
        LIB_LOCATION = '../Libraries/libjvm.dylib'
        INCLUDE_DIRS = [join(
            FRAMEWORK, (
                'System/Library/Frameworks/'
                'JavaVM.framework/Versions/Current/Headers'
            )
        )]
    else:
        LIB_LOCATION = 'jre/lib/server/libjvm.dylib'

        # We want to favor Java installation declaring JAVA_HOME
        if getenv('JAVA_HOME'):
            FRAMEWORK = getenv('JAVA_HOME')

        FULL_LIB_LOCATION = join(FRAMEWORK, LIB_LOCATION)

        if not exists(FULL_LIB_LOCATION):
            # In that case, the Java version is very likely >=9.
            # So we need to modify the `libjvm.so` path.
            LIB_LOCATION = 'lib/server/libjvm.dylib'

        INCLUDE_DIRS = [
            '{0}/include'.format(FRAMEWORK),
            '{0}/include/darwin'.format(FRAMEWORK)
        ]

    print('JAVA_HOME: {0}\n'.format(FRAMEWORK))

    compile_native_invocation_handler(FRAMEWORK)

else:
    # Note: if on Windows, set ONLY JAVA_HOME
    # not on android or osx, we need to search the JDK_HOME

    JDK_HOME = getenv('JDK_HOME')
    if not JDK_HOME:

        if PLATFORM == 'win32':
            TMP_JDK_HOME = getenv('JAVA_HOME')
            print(TMP_JDK_HOME)
            if not TMP_JDK_HOME:
                raise Exception('Unable to find JAVA_HOME')

            # Remove /bin if it's appended to JAVA_HOME
            if TMP_JDK_HOME[-3:] == 'bin':
                TMP_JDK_HOME = TMP_JDK_HOME[:-4]

            # Check whether it's JDK
            if exists(join(TMP_JDK_HOME, 'bin', 'javac.exe')):
                JDK_HOME = TMP_JDK_HOME

        else:
            JDK_HOME = realpath(
                subprocess.check_output(
                    ['which', 'javac']
                ).decode('utf-8').strip()
            ).replace('bin/javac', '')

    if not JDK_HOME or not exists(JDK_HOME):
        raise Exception('Unable to determine JDK_HOME')

    JRE_HOME = None
    if exists(join(JDK_HOME, 'jre')):
        JRE_HOME = join(JDK_HOME, 'jre')

    if PLATFORM != 'win32' and not JRE_HOME:
        JRE_HOME = realpath(
            subprocess.check_output(
                ['which', 'java']
            ).decode('utf-8').strip()
        ).replace('bin/java', '')

    # This dictionary converts values from platform.machine()
    # to a "cpu" string. It is needed to set the correct lib path,
    # found in the JRE_HOME, e.g.: <JRE_HOME>/lib/<cpu>/.
    MACHINE2CPU = {
        "i686": "i386",
        "x86_64": "amd64",
        "armv7l": "arm"
    }
    if machine() in MACHINE2CPU.keys():
        CPU = MACHINE2CPU[machine()]
    else:
        print(
            "WARNING: Not able to assign machine()"
            " = %s to a cpu value!" % machine()
        )
        print("         Using cpu = 'i386' instead!")
        CPU = 'i386'

    if PLATFORM == 'win32':
        INCL_DIR = join(JDK_HOME, 'include', 'win32')
        LIBRARIES = ['jvm']
    else:
        INCL_DIR = join(JDK_HOME, 'include', 'linux')
        LIB_LOCATION = 'jre/lib/{}/server/libjvm.so'.format(CPU)

        if isinstance(JRE_HOME, bytes):
            JAVA_HOME = dirname(JRE_HOME.decode())
        else:
            JAVA_HOME = dirname(JRE_HOME)
        FULL_LIB_LOCATION = join(JAVA_HOME, LIB_LOCATION)

        if not exists(FULL_LIB_LOCATION):
            # In that case, the Java version is very likely >=9.
            # So we need to modify the `libjvm.so` path.
            LIB_LOCATION = 'lib/server/libjvm.so'

    INCLUDE_DIRS = [
        join(JDK_HOME, 'include'),
        INCL_DIR
    ]

    if PLATFORM == 'win32':

        if isinstance(JRE_HOME, bytes):
            JRE_HOME = JRE_HOME.decode('utf-8')

        LIBRARY_DIRS = [
            join(JDK_HOME, 'lib'),
            join(JDK_HOME, 'bin', 'server')
        ]

    print('JDK_HOME: {0}\n'.format(JDK_HOME))
    print('JRE_HOME: {0}\n'.format(JRE_HOME))

    compile_native_invocation_handler(JDK_HOME, JRE_HOME)

# generate the config.pxi
with open(join(dirname(__file__), 'jnius', 'config.pxi'), 'w') as fd:
    fd.write('DEF JNIUS_PLATFORM = {0!r}\n\n'.format(PLATFORM))
    if not PY2:
        fd.write('DEF JNIUS_PYTHON3 = True\n\n')
    else:
        fd.write('DEF JNIUS_PYTHON3 = False\n\n')
    if LIB_LOCATION is not None:
        fd.write('DEF JNIUS_LIB_SUFFIX = {0!r}\n\n'.format(LIB_LOCATION))

# pop setup.py from included files in the installed package
SETUP_KWARGS['py_modules'].remove('setup')

# create the extension
setup(
    cmdclass={'build_ext': build_ext},
    install_requires=INSTALL_REQUIRES,
    ext_modules=[
        Extension(
            'jnius', [join('jnius', x) for x in FILES],
            libraries=LIBRARIES,
            library_dirs=LIBRARY_DIRS,
            include_dirs=INCLUDE_DIRS,
            extra_link_args=EXTRA_LINK_ARGS
        )
    ],
    **SETUP_KWARGS
)
