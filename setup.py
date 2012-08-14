from distutils.core import setup, Extension
from os import environ
from os.path import dirname, join
import sys

libraries = []
library_dirs = []
extra_link_args = []
include_dirs = []

# detect Python for android
platform = sys.platform
ndkplatform = environ.get('NDKPLATFORM')
if ndkplatform is not None and environ.get('LIBLINK'):
    platform = 'android'

# detect cython
try:
    from Cython.Distutils import build_ext
    have_cython = True
    ext = 'pyx'
except ImportError:
    from distutils.command.build_ext import build_ext
    have_cython = False
    ext = 'c'

if platform == 'android':
    # for android, we use SDL...
    libraries = ['sdl', 'log']
    library_dirs = ['libs/' + environ['ARCH']]
else:
    import subprocess
    # otherwise, we need to search the JDK_HOME
    jdk_home = environ.get('JDK_HOME')
    if not jdk_home:
        jdk_home = subprocess.Popen('readlink -f /usr/bin/javac | sed "s:bin/javac::"',
                shell=True, stdout=subprocess.PIPE).communicate()[0].strip()
    if not jdk_home:
        raise Exception('Unable to determine JDK_HOME')

    jre_home = environ.get('JRE_HOME')
    if not jre_home:
        jre_home = subprocess.Popen('readlink -f /usr/bin/java | sed "s:bin/java::"',
                shell=True, stdout=subprocess.PIPE).communicate()[0].strip()
    if not jre_home:
        raise Exception('Unable to determine JRE_HOME')
    cpu = 'i386' if sys.maxint == 2147483647 else 'amd64'
    include_dirs = [
            join(jdk_home, 'include'),
            join(jdk_home, 'include', 'linux')]
    library_dirs = [join(jre_home, 'lib', cpu, 'server')]
    extra_link_args = ['-Wl,-rpath', library_dirs[0]]
    libraries = ['jvm']

# generate the config.pxi
with open(join(dirname(__file__), 'jnius', 'config.pxi'), 'w') as fd:
    fd.write('DEF JNIUS_PLATFORM = {0!r}'.format(platform))

# create the extension
setup(name='jnius',
      version='1.0',
      cmdclass={'build_ext': build_ext},
      packages=['jnius'],
      ext_package='jnius',
      ext_modules=[
          Extension(
              'jnius', ['jnius/jnius.' + ext],
              libraries=libraries,
              library_dirs=library_dirs,
              include_dirs=include_dirs,
              extra_link_args=extra_link_args)
          ]
      )
