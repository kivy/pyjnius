from __future__ import print_function
from distutils.core import setup, Extension
from os import environ
from os.path import dirname, join, exists
import sys
from platform import architecture

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
extra_link_args = []
include_dirs = []
install_requires = []

# detect Python for android
platform = sys.platform
ndkplatform = environ.get('NDKPLATFORM')
if ndkplatform is not None and environ.get('LIBLINK'):
    platform = 'android'

# detect cython
try:
    from Cython.Distutils import build_ext
    install_requires.append('cython')
except ImportError:
    from distutils.command.build_ext import build_ext
    if platform != 'android':
        print('\n\nYou need Cython to compile Pyjnius.\n\n')
        raise
    # On Android we expect to see 'c' files lying about.
    # and we go ahead with the 'desktop' file? Odd.
    files = [fn[:-3] + 'c' for fn in files if fn.endswith('pyx')]

if platform == 'android':
    # for android, we use SDL...
    libraries = ['sdl', 'log']
    library_dirs = ['libs/' + environ['ARCH']]
elif platform == 'darwin':
    import subprocess
    # That decode won't work in Py2?
    framework = subprocess.Popen('/usr/libexec/java_home',
            shell=True, stdout=subprocess.PIPE).communicate()[0].decode().strip()
    print('java_home: {0}\n'.format(framework));
    if not framework:
        raise Exception('You must install Java on your Mac OS X distro')
    if '1.6' in framework:
        lib_location = '../Libraries/libjvm.dylib'
        include_dirs = [join(framework, 'System/Library/Frameworks/JavaVM.framework/Versions/Current/Headers')]
    else:
        lib_location = 'jre/lib/server/libjvm.dylib'
        include_dirs = ['{0}/include'.format(framework), '{0}/include/darwin'.format(framework)]

else:
    import subprocess
    # otherwise, we need to search the JDK_HOME
    jdk_home = environ.get('JDK_HOME')
    if not jdk_home:
        if platform == 'win32':
            env_var = environ.get('JAVA_HOME')
            if env_var and 'jdk' in env_var:
                jdk_home = env_var

                # Remove /bin if it's appended to JAVA_HOME
                if jdk_home[-3:] == 'bin':
                    jdk_home = jdk_home[:-4]
        else:
            jdk_home = subprocess.Popen('readlink -f `which javac` | sed "s:bin/javac::"',
                    shell=True, stdout=subprocess.PIPE).communicate()[0].strip()
    if not jdk_home or not exists(jdk_home):
        raise Exception('Unable to determine JDK_HOME')

    jre_home = environ.get('JRE_HOME')
    if exists(join(jdk_home, 'jre')):
        jre_home = join(jdk_home, 'jre')
    if not jre_home:
        jre_home = subprocess.Popen('readlink -f `which java` | sed "s:bin/java::"',
                shell=True, stdout=subprocess.PIPE).communicate()[0].strip()
    if not jre_home:
        raise Exception('Unable to determine JRE_HOME')
    cpu = 'amd64' if architecture()[0] == '64bit' else 'i386'

    if platform == 'win32':
        incl_dir = join(jdk_home, 'include', 'win32')
        libraries = ['jvm']
    else:
        incl_dir = join(jdk_home, 'include', 'linux')
        lib_location = 'jre/lib/amd64/server/libjvm.so'

    include_dirs = [
            join(jdk_home, 'include'),
            incl_dir]

    if platform == 'win32':
        library_dirs = [
                join(jdk_home, 'lib'),
                join(jre_home, 'bin', 'server')]

# generate the config.pxi
with open(join(dirname(__file__), 'jnius', 'config.pxi'), 'w') as fd:
    fd.write('DEF JNIUS_PLATFORM = {0!r}\n\n'.format(platform))
    if sys.version_info>=(3,0,0):
        fd.write('DEF JNIUS_PYTHON3 = True\n\n')
    else:
        fd.write('DEF JNIUS_PYTHON3 = False\n\n')
    if lib_location is not None:
        fd.write('DEF JNIUS_LIB_SUFFIX = {0!r}\n\n'.format(lib_location))

with open(join('jnius', '__init__.py')) as fd:
    versionline = [x for x in fd.readlines() if x.startswith('__version__')]
    version = versionline[0].split("'")[-2]

# create the extension
setup(name='jnius',
      version=version,
      cmdclass={'build_ext': build_ext},
      packages=['jnius'],
      py_modules=['jnius_config'],
      url='http://pyjnius.readthedocs.org/',
      author='Mathieu Virbel and Gabriel Pettier',
      author_email='mat@kivy.org,gabriel@kivy.org',
      license='LGPL',
      description='Python library to access Java classes',
      install_requires=install_requires,
      ext_package='jnius',
      ext_modules=[
          Extension(
              'jnius', [join('jnius', x) for x in files],
              libraries=libraries,
              library_dirs=library_dirs,
              include_dirs=include_dirs,
              extra_link_args=extra_link_args)
          ],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks'])
