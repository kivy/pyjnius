from distutils.core import setup, Extension
from os import environ
from os.path import dirname, join, exists
import sys

files = [
    'jni.pxi',
    'jnius_conversion.pxi',
    'jnius_export_class.pxi',
    'jnius_export_func.pxi',
    'jnius_jvm_android.pxi',
    'jnius_jvm_desktop.pxi',
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
except ImportError:
    from distutils.command.build_ext import build_ext
    if platform != 'android':
        print('\n\nWarning: You need Cython to compile Pyjnius.\n\n')
    files = [fn[:-3] + 'c' for fn in files if fn.endswith('pyx')]

if platform == 'android':
    # for android, we use SDL...
    libraries = ['sdl', 'log']
    library_dirs = ['libs/' + environ['ARCH']]
elif platform == 'darwin':
    
    try:
        import objc
        framework = objc.pathForFramework('JavaVM.framework')
        if not framework:
            raise Exception('You must install Java on your Mac OS X distro')
        extra_link_args = ['-framework', 'JavaVM']
        include_dirs = [join(framework, 'Versions/A/Headers')]
    except ImportError:
        import subprocess
        java_home = subprocess.check_output('/usr/libexec/java_home').strip()
        print(java_home)
        library_dirs = [join(java_home, 'jre', 'lib', 'server')]
        libraries = ['jvm']
        extra_link_args = ['-Wl,-rpath', library_dirs[0]]
        include_dirs = [join(java_home, 'include'), join(java_home, 'include', 'darwin')]
elif platform == 'win32':
    jdk_home = environ.get('JDK_HOME')
    jre_home = environ.get('JRE_HOME')
    include_dirs = [ join(jdk_home, 'include'), join(jdk_home, 'include', platform)]
    library_dirs = [ join(jdk_home, 'lib') ]
    libraries = ['jvm'] 
elif platform == 'linux2':
    import subprocess
    # otherwise, we need to search the JDK_HOME
    jdk_home = environ.get('JDK_HOME')
    library_dirs = [join(jre_home, 'lib', cpu, 'server')]
    extra_link_args = ['-Wl,-rpath', library_dirs[0]]
    libraries = ['jvm']
else:
    raise Exception("Unsupported platform {}".format(platform))

# generate the config.pxi
with open(join(dirname(__file__), 'jnius', 'config.pxi'), 'w') as fd:
    fd.write('DEF JNIUS_PLATFORM = {0!r}'.format(platform))

with open(join('jnius', '__init__.py')) as fd:
    versionline = [x for x in fd.readlines() if x.startswith('__version__')]
    version = versionline[0].split("'")[-2]

# create the extension
setup(name='phyjnius',
      version=version,
      cmdclass={'build_ext': build_ext},
      packages=['jnius'],
      url='https://github.com/physion/pyjnius',
      author='Physion LLC. Original pyjnius code by Mathieu Virbel and Gabriel Pettier',
      author_email='dev@physion.us',
      license='LGPL',
      description='Python library to access Java classes',
      install_requires=install_requires,
      setup_requires=['Cython>=0.19.1'],
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
        'License :: OSI Approved :: GNU Library or Lesser '
        'General Public License (LGPL)',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks'])
