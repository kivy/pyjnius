'''
Setup.py for creating a binary distribution.
'''

from os import environ
from os.path import dirname, join
import subprocess
import sys

from setup_sdist import SETUP_KWARGS
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


# import jnius_config.env withough having build
syspath = sys.path[:]
sys.path.insert(0, 'jnius_config')
from env import get_java_setup
sys.path = syspath

def getenv(key):
    '''Get value from environment and decode it.'''
    val = environ.get(key)
    if val is not None:
        try:
            return val.decode()
        except AttributeError:
            return val
    return val


PYX_FILES = [
    'jnius.pyx',
]
PXI_FILES = [
    'jnius_compat.pxi',
    'jnius_conversion.pxi',
    'jnius_export_class.pxi',
    'jnius_export_func.pxi',
    'jnius_jvm_android.pxi',
    'jnius_jvm_desktop.pxi',
    'jnius_jvm_dlopen.pxi',
    'jnius_localref.pxi',
    'jnius_nativetypes3.pxi',
    'jnius_proxy.pxi',
    'jnius.pyx',
    'jnius_utils.pxi'
]

EXTRA_LINK_ARGS = []

# detect Python for android
PLATFORM = sys.platform
NDKPLATFORM = getenv('NDKPLATFORM')
if NDKPLATFORM is not None and getenv('LIBLINK'):
    PLATFORM = 'android'

# detect platform
if PLATFORM == 'android':
    PYX_FILES = [fn[:-3] + 'c' for fn in PYX_FILES]

JAVA=get_java_setup(PLATFORM)

# The Android wheel is Java-free: the org.jnius.NativeInvocationHandler glue is
# supplied and dex'd by the host app (e.g. a Kivy/kivyforge bootstrap), never by the
# wheel -- a class in site-packages is not on ART's dex classpath, so a bundled
# .class/.java would be inert. Android therefore needs no javac/JDK and ships no Java
# (see the package_data prune below). Desktop is unchanged: it still requires a JDK to
# compile and bundle NativeInvocationHandler.class, which its self-hosted JVM loads.
if PLATFORM != 'android':
    assert JAVA.is_jdk(), "You need a JDK, we only found a JRE. Try setting JAVA_HOME"


def compile_native_invocation_handler(java):
    '''Find javac and compile NativeInvocationHandler.java.'''
    javac = java.get_javac()
    source_level = '8'
    try:
        subprocess.check_call([
            javac, '-target', source_level, '-source', source_level,
            join('jnius', 'src', 'org', 'jnius', 'NativeInvocationHandler.java')
        ])
    except FileNotFoundError:
        subprocess.check_call([
            javac.replace('"', ''), '-target', source_level, '-source', source_level,
            join('jnius', 'src', 'org', 'jnius', 'NativeInvocationHandler.java')
        ])


if PLATFORM != 'android':
    compile_native_invocation_handler(JAVA)


# generate the config.pxi
with open(join(dirname(__file__), 'jnius', 'config.pxi'), 'w') as fd:
    fd.write('DEF JNIUS_PLATFORM = {0!r}\n\n'.format(PLATFORM))

# pop setup.py from included files in the installed package
SETUP_KWARGS['py_modules'].remove('setup')

# Make the Android wheel truly Java-free: drop the org.jnius glue from package_data so
# neither the .java source nor a .class ships (it would be inert on Android anyway).
# The canonical source stays in the repo/sdist for any packager that needs it.
if PLATFORM == 'android':
    SETUP_KWARGS['package_data'] = {
        pkg: [p for p in patterns if not p.startswith('src/org')]
        for pkg, patterns in SETUP_KWARGS.get('package_data', {}).items()
    }

ext_modules = [
    Extension(
        'jnius', 
        [join('jnius', x) for x in PYX_FILES],
        depends=[join('jnius', x) for x in PXI_FILES],
        libraries=JAVA.get_libraries(),
        library_dirs=JAVA.get_library_dirs(),
        include_dirs=JAVA.get_include_dirs(),
        extra_link_args=EXTRA_LINK_ARGS,
    )
]

for ext_mod in ext_modules:
    ext_mod.cython_directives = {'language_level': 3}


# create the extension
setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
    **SETUP_KWARGS
)
