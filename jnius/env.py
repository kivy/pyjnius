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


PY2 = sys.version_info.major < 3

machine = machine()  # not expected to change at runtime

# This dictionary converts values from platform.machine()
# to a "cpu" string. It is needed to set the correct lib path,
# found in the JRE_HOME, e.g.: <JRE_HOME>/lib/<cpu>/.
MACHINE2CPU = {
    "i686": "i386",
    "x86_64": "amd64",
    "AMD64": "amd64",
    "armv7l": "arm",
    "sun4u": "sparcv9",
    "sun4v": "sparcv9"
}

JAVA_HOME = getenv('JAVA_HOME')


def find_javac(platform, possible_homes):
    '''Find javac in all possible locations.'''
    name = "javac.exe" if platform == "win32" else "javac"
    for home in possible_homes:
        for javac in [join(home, name), join(home, 'bin', name)]:
            if exists(javac):
                if platform == "win32" and not PY2:  # Avoid path space execution error
                    return '"%s"' % javac
                return javac
    return name  # Fall back to "hope it's on the path"


def get_include_dirs(platform):
    if platform == 'darwin':
        framework = get_osx_framework()
        if '1.6' in framework:
            return [join(
                framework, (
                    'System/Library/Frameworks/'
                    'JavaVM.framework/Versions/Current/Headers'
                )
            )]
        else:
            # We want to favor Java installation declaring JAVA_HOME
            if JAVA_HOME:
                framework = JAVA_HOME

            return [
                '{0}/include'.format(framework),
                '{0}/include/darwin'.format(framework)
            ]

    else:
        jdk_home = get_jdk_home(platform)
        if platform == 'win32':
            incl_dir = join(jdk_home, 'include', 'win32')
        elif platform == 'sunos5':
            incl_dir = join(jdk_home, 'include', 'solaris')
        else:
            incl_dir = join(jdk_home, 'include', 'linux')

        return [
            join(jdk_home, 'include'),
            incl_dir
        ]

def get_library_dirs(platform, arch=None):
    if platform == 'win32':
        jre_home = get_jre_home(platform)
        jdk_home = JAVA_HOME

        if isinstance(jre_home, bytes):
            jre_home = jre_home.decode('utf-8')

        return [
            join(jdk_home, 'lib'),
            join(jdk_home, 'bin', 'server')
        ]
    elif platform == 'android':
        return ['libs/{}'.format(arch)]
    return []


def get_jre_home(platform):
    jre_home = None
    if JAVA_HOME and exists(join(JAVA_HOME, 'jre')):
        jre_home = join(JAVA_HOME, 'jre')

    if platform != 'win32' and not jre_home:
        jre_home = realpath(
            check_output(
                split('which java')
            ).decode('utf-8').strip()
        ).replace('bin/java', '')

    if platform == 'win32':
        if isinstance(jre_home, bytes):
            jre_home = jre_home.decode('utf-8')

    return jre_home


def get_jdk_home(platform):
    jdk_home = getenv('JDK_HOME')
    if not jdk_home:
        if platform == 'win32':
            TMP_JDK_HOME = getenv('JAVA_HOME')
            print(TMP_JDK_HOME)
            if not TMP_JDK_HOME:
                raise Exception('Unable to find JAVA_HOME')

            # Remove /bin if it's appended to JAVA_HOME
            if TMP_JDK_HOME[-3:] == 'bin':
                TMP_JDK_HOME = TMP_JDK_HOME[:-4]

            # Check whether it's JDK
            if exists(join(TMP_JDK_HOME, 'bin', 'javac.exe')):
                jdk_home = TMP_JDK_HOME

        else:
            jdk_home = realpath(
                check_output(
                    ['which', 'javac']
                ).decode('utf-8').strip()
            ).replace('bin/javac', '')

    if not jdk_home or not exists(jdk_home):
        raise Exception('Unable to determine JDK_HOME')

    return jdk_home


def get_osx_framework():
    framework = Popen(
        '/usr/libexec/java_home',
        stdout=PIPE, shell=True
    ).communicate()[0]

    if not PY2:
        framework = framework.decode('utf-8')

    return framework.strip()


def get_possible_homes(platform):
    if platform == 'darwin':
        if JAVA_HOME:
            return JAVA_HOME

        FRAMEWORK = get_osx_framework()
        if not FRAMEWORK:
            raise Exception('You must install Java for Mac OSX')

        return FRAMEWORK

    else:
        return (
            get_jdk_home(platform),
            get_jre_home(platform),
        )


def get_cpu():
    try:
        return MACHINE2CPU[machine]
    except KeyError:
        print(
            "WARNING: Not able to assign machine()"
            " = %s to a cpu value!" % machine
        )
        print("         Using cpu = 'i386' instead!")
        return 'i386'


def get_libraries(platform):
    if platform == 'android':
        # for android, we use SDL...
        return ['sdl', 'log']

    elif platform == 'win32':
        return ['jvm']


def get_jnius_lib_location(platform):
    cpu = get_cpu()

    if platform == 'darwin':
        framework = get_osx_framework()

        if '1.6' in framework:
            return '../Libraries/libjvm.dylib'

        else:
            lib_location = 'jre/lib/jli/libjli.dylib'

            # We want to favor Java installation declaring JAVA_HOME
            if JAVA_HOME:
                framework = JAVA_HOME

            full_lib_location = join(framework, lib_location)

            if not exists(full_lib_location):
                # In that case, the Java version is very likely >=9.
                # So we need to modify the `libjvm.so` path.
                lib_location = 'lib/jli/libjli.dylib'
                full_lib_location = join(framework, lib_location)

            if not exists(full_lib_location):
                # adoptopenjdk12 doesn't have the jli subfolder either
                return 'lib/libjli.dylib'

            return lib_location

    elif platform == 'sunos5':
        return 'jre/lib/{}/server/libjvm.so'.format(cpu)

    else:
        if platform not in ('linux', 'linux2'):
            print("warning: unknown platform assuming linux")

        lib_location = 'jre/lib/{}/server/libjvm.so'.format(cpu)

        jre_home = dirname(get_jre_home(platform)).strip('jre')

        full_lib_location = join(jre_home, lib_location)

        if not exists(full_lib_location):
            # In that case, the Java version is very likely >=9.
            # So we need to modify the `libjvm.so` path.
            lib_location = 'lib/server/libjvm.so'
        return lib_location
