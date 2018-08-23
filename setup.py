from __future__ import print_function
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension
try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess
from os import environ
from os.path import dirname, join, exists
import sys
from platform import machine

PY3 = sys.version_info >= (3, 0, 0)


def getenv(key):
    val = environ.get(key)
    if val is not None:
        if PY3:
            try:
                return val.decode()
            except AttributeError:
                return val
    return val


files = [
    'jni.pxi',
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

libraries = []
library_dirs = []
lib_location = None
extra_link_args = []
include_dirs = []
install_requires = ['six>=1.7.0']

# detect Python for android
platform = sys.platform
ndkplatform = getenv('NDKPLATFORM')
if ndkplatform is not None and getenv('LIBLINK'):
    platform = 'android'

# detect cython
try:
    from Cython.Distutils import build_ext
    install_requires.append('cython')
except ImportError:
    try:
        from setuptools.command.build_ext import build_ext
    except ImportError:
        from distutils.command.build_ext import build_ext
    if platform != 'android':
        print('\n\nYou need Cython to compile Pyjnius.\n\n')
        raise
    # On Android we expect to see 'c' files lying about.
    # and we go ahead with the 'desktop' file? Odd.
    files = [fn[:-3] + 'c' for fn in files if fn.endswith('pyx')]

def find_javac(possible_homes):
    name = "javac.exe" if sys.platform == "win32" else "javac"
    for home in possible_homes:
        for javac in [join(home, name), join(home, 'bin', name)]:
            if exists(javac):
                return javac
    return name  # Fall back to "hope it's on the path"


def compile_native_invocation_handler(*possible_homes):
    javac = find_javac(possible_homes)
    subprocess.check_call([
        javac, '-target', '1.6', '-source', '1.6',
        join('jnius', 'src', 'org', 'jnius', 'NativeInvocationHandler.java')
    ])


if platform == 'android':
    # for android, we use SDL...
    libraries = ['sdl', 'log']
    library_dirs = ['libs/' + getenv('ARCH')]
elif platform == 'darwin':
    framework = subprocess.Popen(
        '/usr/libexec/java_home',
        stdout=subprocess.PIPE, shell=True).communicate()[0]
    if PY3:
        framework = framework.decode()
    framework = framework.strip()
    print('java_home: {0}\n'.format(framework))
    if not framework:
        raise Exception('You must install Java on your Mac OS X distro')
    if '1.6' in framework:
        lib_location = '../Libraries/libjvm.dylib'
        include_dirs = [join(framework, 'System/Library/Frameworks/JavaVM.framework/Versions/Current/Headers')]
    else:
        lib_location = 'jre/lib/server/libjvm.dylib'
        include_dirs = [
            '{0}/include'.format(framework),
            '{0}/include/darwin'.format(framework)
        ]
    compile_native_invocation_handler(framework)
else:
    # otherwise, we need to search the JDK_HOME
    jdk_home = getenv('JDK_HOME')
    if not jdk_home:
        if platform == 'win32':
            env_var = getenv('JAVA_HOME')
            if env_var and 'jdk' in env_var:
                jdk_home = env_var

                # Remove /bin if it's appended to JAVA_HOME
                if jdk_home[-3:] == 'bin':
                    jdk_home = jdk_home[:-4]
        else:
            jdk_home = subprocess.Popen(
                'readlink -f `which javac` | sed "s:bin/javac::"',
                shell=True, stdout=subprocess.PIPE).communicate()[0].strip()
            if jdk_home is not None and PY3:
                jdk_home = jdk_home.decode()
    if not jdk_home or not exists(jdk_home):
        raise Exception('Unable to determine JDK_HOME')

    jre_home = getenv('JRE_HOME')
    if jre_home is None:
        if exists(join(jdk_home, 'jre')):
            jre_home = join(jdk_home, 'jre')
        if not jre_home:
            jre_home = subprocess.Popen(
                'readlink -f `which java` | sed "s:bin/java::"',
                shell=True, stdout=subprocess.PIPE).communicate()[0].strip()
    if not jre_home or not exists(jre_home):
        raise Exception('Unable to determine JRE_HOME')

    # This dictionary converts values from platform.machine() to a "cpu" string.
    # It is needed to set the correct lib path, found in the jre_home, eg.
    # <jre_home>/lib/<cpu>/.
    machine2cpu = {
        "i686" : "i386",
        "x86_64" : "amd64",
        "armv7l" : "arm"
    }
    if machine() in machine2cpu.keys():
        cpu = machine2cpu[machine()]
    else:
        print("WARNING: Not able to assign machine() = %s to a cpu value!" %(machine()))
        print("         Using cpu = 'i386' instead!")
        cpu = 'i386'

    if platform == 'win32':
        incl_dir = join(jdk_home, 'include', 'win32')
        libraries = ['jvm']
    else:
        incl_dir = join(jdk_home, 'include', 'linux')
        lib_location = 'jre/lib/{}/server/libjvm.so'.format(cpu)

    include_dirs = [
        join(jdk_home, 'include'),
        incl_dir
    ]

    if platform == 'win32':
        library_dirs = [
            join(jdk_home, 'lib'),
            join(jre_home, 'bin', 'server')
        ]

    compile_native_invocation_handler(jdk_home, jre_home)

# generate the config.pxi
with open(join(dirname(__file__), 'jnius', 'config.pxi'), 'w') as fd:
    fd.write('DEF JNIUS_PLATFORM = {0!r}\n\n'.format(platform))
    if PY3:
        fd.write('DEF JNIUS_PYTHON3 = True\n\n')
    else:
        fd.write('DEF JNIUS_PYTHON3 = False\n\n')
    if lib_location is not None:
        fd.write('DEF JNIUS_LIB_SUFFIX = {0!r}\n\n'.format(lib_location))

with open(join('jnius', '__init__.py')) as fd:
    versionline = [x for x in fd.readlines() if x.startswith('__version__')]
    version = versionline[0].split("'")[-2]

# create the extension
setup(
    name='pyjnius',
    version=version,
    cmdclass={'build_ext': build_ext},
    packages=['jnius'],
    py_modules=['jnius_config'],
    url='https://pyjnius.readthedocs.io',
    author='Kivy Team and other contributors',
    author_email='kivy-dev@googlegroups.com',
    license='MIT',
    description='Dynamic access to Java classes from Python',
    install_requires=install_requires,
    ext_package='jnius',
    ext_modules=[
        Extension(
            'jnius', [join('jnius', x) for x in files],
            libraries=libraries,
            library_dirs=library_dirs,
            include_dirs=include_dirs,
            extra_link_args=extra_link_args
        )
    ],
    package_data={
        'jnius': [ 'src/org/jnius/*' ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ]
)
