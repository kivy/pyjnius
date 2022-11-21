'''
This module determine and expose various information about the java
environment.
'''

import sys
from os.path import join, exists, dirname, realpath
from os import getenv
from platform import machine
from subprocess import Popen, check_output, PIPE
from shlex import split
import logging
from textwrap import dedent
from shutil import which

log = logging.getLogger('kivy').getChild(__name__)

machine = machine()  # not expected to change at runtime

# This dictionary converts values from platform.machine()
# to a "cpu" string. It is needed to set the correct lib path,
# found in the JRE_HOME, e.g.: <JRE_HOME>/lib/<cpu>/.
MACHINE2CPU = {
    "i686": "i386",
    "x86_64": "amd64",
    "AMD64": "amd64",
    "armv7l": "arm",
    "aarch64": "aarch64",
    "sun4u": "sparcv9",
    "sun4v": "sparcv9"
}

DEFAULT_PLATFORM = sys.platform


def is_set(string):
    return string is not None and len(string) > 0


def get_java_setup(platform=DEFAULT_PLATFORM):
    '''
        Returns an instance of JavaLocation. 
    '''
    # prefer Env variables
    JAVA_HOME = getenv('JAVA_HOME')
    if not is_set(JAVA_HOME):
        JAVA_HOME = getenv('JDK_HOME')
    if not is_set(JAVA_HOME):
        JAVA_HOME = getenv('JRE_HOME')
    #TODO encodings

    # Use java_home program on Mac
    if not is_set(JAVA_HOME) and platform == 'darwin':
        JAVA_HOME = get_osx_framework()
        if not is_set(JAVA_HOME):
            raise Exception('You must install Java for Mac OSX')

    # go hunting for Javac and Java programs, in that order
    if not is_set(JAVA_HOME):
        JAVA_HOME = get_jdk_home(platform)

    if not is_set(JAVA_HOME):
        JAVA_HOME = get_jre_home(platform)

    if JAVA_HOME is None:
        raise RuntimeError("Could not find your Java installed. Please set the JAVA_HOME env var.")

    if isinstance(JAVA_HOME, bytes):
        JAVA_HOME = JAVA_HOME.decode('utf-8')

    log.debug("Identified Java at %s" % JAVA_HOME)

    # Remove /bin if it's appended to JAVA_HOME
    if JAVA_HOME[-3:] == 'bin':
        JAVA_HOME = JAVA_HOME[:-4]

    if platform == "android":
        return AndroidJavaLocation(platform, JAVA_HOME)
    if platform == "win32": #only this?
        return WindowsJavaLocation(platform, JAVA_HOME)
    if platform == "darwin": #only this?
        return MacOsXJavaLocation(platform, JAVA_HOME)    
    if 'bsd' in platform:
        return BSDJavaLocation(platform, JAVA_HOME)
    if platform in ('linux', 'linux2', 'sunos5'): #only this?
        return UnixJavaLocation(platform, JAVA_HOME)
    log.warning("warning: unknown platform %s assuming linux or sunOS" % platform)
    return UnixJavaLocation(platform, JAVA_HOME)


class JavaLocation:
    def __init__(self, platform, home):
        self.platform = platform
        self.home = home

    def get_javahome(self):
        '''
            Returns the location of the identified JRE or JDK
        '''
        return self.home


    def is_jdk(self):
        '''
            Returns true if the location is a JDK, based on existing of javac
        '''
        javac = self.get_javac()
        return exists(javac)

    def get_javac(self): 
        '''
            Returns absolute path of the javac executable
        '''
        return join(self.home, "bin", "javac")

    def get_include_dirs(self):
        '''
            Returns a list of absolute paths of JDK include directories, for compiling.
            Calls _get_platform_include_dir() internally.
        ''' 
        return [
            join(self.home, 'include'),
            self._get_platform_include_dir()
        ]

    def _get_platform_include_dir(self):
        '''
            Returns the platform-specific include directory, for setup.py
        '''
        pass

    def get_library_dirs(self): 
        '''
            Returns a list of absolute paths of JDK lib directories, for setup.py
        '''
        pass

    def get_libraries(self): 
        '''
            Returns the names of the libraries for this platform, for setup.py
        '''
        pass

    def get_jnius_lib_location(self): 
        '''
            Returns the full path of the Java library for runtime binding with.
            Can be overridden by using JVM_PATH env var to set absolute path of the Java library
        '''
        libjvm_override_path = getenv('JVM_PATH')
        if libjvm_override_path:
            log.info(
                dedent("""
                    Using override env var JVM_PATH (%s) to load libjvm.
                    Please report your system information (os version, java
                    version, etc), and the path that works for you, to the
                    PyJNIus project, at https://github.com/kivy/pyjnius/issues.
                    so we can improve the automatic discovery.
                """
                ),
                libjvm_override_path
            )
            return libjvm_override_path

        platform = self.platform
        log.debug("looking for libjvm to initiate pyjnius, platform is %s", platform)
        lib_locations = self._possible_lib_locations()
        for location in lib_locations:
            full_lib_location = join(self.home, location)
            if exists(full_lib_location):
                log.debug("found libjvm.so at %s", full_lib_location)
                return full_lib_location

        raise RuntimeError(
        """
        Unable to find libjvm.so, (tried %s)
        you can use the JVM_PATH env variable with the absolute path
        to libjvm.so to override this lookup, if you know
        where pyjnius should look for it.

        e.g:
            export JAVA_HOME=/usr/lib/jvm/java-8-oracle/
            export JVM_PATH=/usr/lib/jvm/java-8-oracle/jre/lib/amd64/server/libjvm.so
            # run your program
        """
        % [join(self.home, loc) for loc in lib_locations]
    )

    def _possible_lib_locations(self):
        '''
            Returns a list of relative possible locations for the Java library.
            Used by the default implementation of get_jnius_lib_location()
        '''
        pass


class WindowsJavaLocation(JavaLocation):
    def get_javac(self):
        return super().get_javac() + ".exe"

    def get_libraries(self):
        return ['jvm']

    def get_library_dirs(self):
        suffices =  ['lib', join('bin', 'server')]
        return [join(self.home, suffix) for suffix in suffices]

    def _get_platform_include_dir(self):
        return join(self.home, 'include', 'win32')


class UnixJavaLocation(JavaLocation):
    def _get_platform_include_dir(self):
        if self.platform == 'sunos5':
            return join(self.home, 'include', 'solaris')
        else:
            return join(self.home, 'include', 'linux')

    def _possible_lib_locations(self):
        root = self.home
        if root.endswith('jre'):
            root = root[:-3]

        cpu = get_cpu()
        log.debug(
            f"Platform {self.platform} may need cpu in path to find libjvm, which is: {cpu}"
        )

        return [
            'lib/server/libjvm.so',
            'jre/lib/{}/default/libjvm.so'.format(cpu),
            'jre/lib/{}/server/libjvm.so'.format(cpu),
        ]


# NOTE: Build works on FreeBSD. Other BSD flavors may need tuning!
class BSDJavaLocation(JavaLocation):
    def _get_platform_include_dir(self):
        os = self.platform.translate({ord(n): None for n in '0123456789'})
        return join(self.home, 'include', os)

    def _possible_lib_locations(self):
        root = self.home
        if root.endswith('jre'):
            root = root[:-3]

        cpu = get_cpu()
        log.debug(
            f"Platform {self.platform} may need cpu in path to find libjvm, which is: {cpu}"
        )

        return [
            'lib/server/libjvm.so',
            'jre/lib/{}/default/libjvm.so'.format(cpu),
            'jre/lib/{}/server/libjvm.so'.format(cpu),
        ]


class MacOsXJavaLocation(UnixJavaLocation):
    def _get_platform_include_dir(self):
        return join(self.home, 'include', 'darwin')

    def _possible_lib_locations(self):
        if '1.6' in self.home:
            return ['../Libraries/libjvm.dylib'] # TODO what should this be resolved to?

        return [
                'jre/lib/jli/libjli.dylib',
                # In that case, the Java version >=9.
                'lib/jli/libjli.dylib',
                # adoptopenjdk12 doesn't have the jli subfolder either
                'lib/libjli.dylib',
        ]



    # this is overridden due to the specifalities of version 1.6
    def get_include_dirs(self):
        framework = self.home
        if '1.6' in framework:
            return [join(
                framework, (
                    'System/Library/Frameworks/'
                    'JavaVM.framework/Versions/Current/Headers'
                )
            )]
        return super().get_include_dirs()


class AndroidJavaLocation(UnixJavaLocation):
    def get_libraries(self):
        return ['SDL2', 'log']

    def get_include_dirs(self):
        # When cross-compiling for Android, we should not use the include dirs
        # exposed by the JDK. Instead, we should use the one exposed by the
        # Android NDK (which are already handled via python-for-android).
        return []

    def get_library_dirs(self):
        return []


def get_jre_home(platform):
    jre_home = None
    if JAVA_HOME and exists(join(JAVA_HOME, 'jre')):
        jre_home = join(JAVA_HOME, 'jre')

    if platform != 'win32' and not jre_home:
        try:
            jre_home = realpath(
                which('java')
            ).replace('bin/java', '')
        except TypeError:
            raise Exception('Unable to find java')

        if is_set(jre_home):
            return jre_home

        # didnt find java command on the path, we can
        # fallback to hunting in some default unix locations
        for loc in ["/usr/java/latest/", "/usr/java/default/", "/usr/lib/jvm/default-java/"]: 
            if exists(loc + "bin/java"):
                jre_home = loc
                break

    return jre_home


def get_jdk_home(platform):
    jdk_home = getenv('JDK_HOME')
    if not jdk_home:
        if platform == 'win32':
            TMP_JDK_HOME = getenv('JAVA_HOME')
            if not TMP_JDK_HOME:
                raise Exception('Unable to find JAVA_HOME')

            # Remove /bin if it's appended to JAVA_HOME
            if TMP_JDK_HOME[-3:] == 'bin':
                TMP_JDK_HOME = TMP_JDK_HOME[:-4]

            # Check whether it's JDK
            if exists(join(TMP_JDK_HOME, 'bin', 'javac.exe')):
                jdk_home = TMP_JDK_HOME

        else:
            try:
                jdk_home = realpath(
                    which('javac')
                ).replace('bin/javac', '')
            except TypeError:
                raise Exception('Unable to find javac')

    if not jdk_home or not exists(jdk_home):
        return None

    return jdk_home


def get_osx_framework():
    framework = Popen(
        '/usr/libexec/java_home',
        stdout=PIPE, shell=True
    ).communicate()[0]

    framework = framework.decode('utf-8')
    return framework.strip()


def get_cpu():
    try:
        return MACHINE2CPU[machine]
    except KeyError:
        print(
            "WARNING: Not able to assign machine()"
            " = %s to a cpu value!" % machine
        )
        print(f"         Using cpu = '{machine}' instead!")
        return machine
