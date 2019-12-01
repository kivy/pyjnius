'''
Setup.py for creating a binary distribution.
'''

from __future__ import print_function
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess

from os import environ
from os.path import dirname, join, exists
import re
import sys
from platform import machine
from setup_sdist import SETUP_KWARGS

# XXX hack to be able to import jnius.env withough having build
# jnius.jnius yet, better solution welcome
syspath = sys.path[:]
sys.path.insert(0, 'jnius')
from env import (
    get_possible_homes,
    get_library_dirs,
    get_include_dirs,
    get_libraries,
    find_javac,
    PY2,
)
sys.path = syspath

def getenv(key):
    '''Get value from environment and decode it.'''
    val = environ.get(key)
    if val is not None and not PY2:
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

EXTRA_LINK_ARGS = []
INSTALL_REQUIRES = ['six>=1.7.0']
SETUP_REQUIRES = []

# detect Python for android
PLATFORM = sys.platform
NDKPLATFORM = getenv('NDKPLATFORM')
if NDKPLATFORM is not None and getenv('LIBLINK'):
    PLATFORM = 'android'

# detect cython
if PLATFORM != 'android':
    SETUP_REQUIRES.append('cython')
    INSTALL_REQUIRES.append('cython')
else:
    FILES = [fn[:-3] + 'c' for fn in FILES if fn.endswith('pyx')]


def compile_native_invocation_handler(*possible_homes):
    '''Find javac and compile NativeInvocationHandler.java.'''
    javac = find_javac(PLATFORM, possible_homes)
    source_level = '1.7'
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

compile_native_invocation_handler(*get_possible_homes(PLATFORM))


# generate the config.pxi
with open(join(dirname(__file__), 'jnius', 'config.pxi'), 'w') as fd:
    fd.write('DEF JNIUS_PLATFORM = {0!r}\n\n'.format(PLATFORM))
    if not PY2:
        fd.write('# cython: language_level=3\n\n')
        fd.write('DEF JNIUS_PYTHON3 = True\n\n')
    else:
        fd.write('# cython: language_level=2\n\n')
        fd.write('DEF JNIUS_PYTHON3 = False\n\n')

# pop setup.py from included files in the installed package
SETUP_KWARGS['py_modules'].remove('setup')

# create the extension
setup(
    cmdclass={'build_ext': build_ext},
    install_requires=INSTALL_REQUIRES,
    setup_requires=SETUP_REQUIRES,
    ext_modules=[
        Extension(
            'jnius', [join('jnius', x) for x in FILES],
            libraries=get_libraries(PLATFORM),
            library_dirs=get_library_dirs(PLATFORM),
            include_dirs=get_include_dirs(PLATFORM),
            extra_link_args=EXTRA_LINK_ARGS,
        )
    ],
    extras_require={
        'dev': ['nose', 'wheel', 'pytest-cov', 'pycodestyle'],
        'ci': ['coveralls', 'pytest-rerunfailures', 'setuptools>=34.4.0'],
    },
    **SETUP_KWARGS
)
