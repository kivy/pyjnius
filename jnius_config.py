__all__ = ('set_options', 'add_options', 'get_options',
           'set_classpath', 'add_classpath', 'get_classpath',
           'expand_classpath')

import platform
if platform.system() == 'Windows':
    split_char = ';'
else:
    split_char = ':'

vm_running = False
vm_started_at = None
options = []
classpath = None


def check_vm_running():
    """Raises a ValueError if the VM is already running."""
    if vm_running:
        raise ValueError("VM is already running, can't set classpath/options; VM started at" + vm_started_at)


def set_options(*opts):
    """Sets the list of options to the JVM. Removes any previously set options."""
    check_vm_running()
    global options
    options = list(opts)


def add_options(*opts):
    """Appends options to the list of VM options."""
    check_vm_running()
    global options
    options.extend(opts)


def get_options():
    """Retrieves the current list of VM options."""
    global options
    return list(options)


def set_classpath(*path):
    """
    Sets the classpath for the JVM to use. Replaces any existing classpath, overriding the CLASSPATH environment variable.
    """
    check_vm_running()
    global classpath
    classpath = list(path)


def add_classpath(*path):
    """
    Appends items to the classpath for the JVM to use.
    Replaces any existing classpath, overriding the CLASSPATH environment variable.
    """
    check_vm_running()
    global classpath
    if classpath is None:
        classpath = list(path)
    else:
        classpath.extend(path)


def get_classpath():
    "Retrieves the classpath the JVM will use."
    from os import environ
    from os.path import realpath
    global classpath

    # add a path to java classes packaged with jnius
    from pkg_resources import resource_filename
    return_classpath = [realpath(resource_filename(__name__, 'jnius/src'))]

    if classpath is not None:
        return_classpath = classpath + return_classpath

    elif 'CLASSPATH' in environ:
        return_classpath = environ['CLASSPATH'].split(split_char) + return_classpath

    else:
        return_classpath = [realpath('.')] + return_classpath

    return return_classpath


def expand_classpath():
    from glob import glob
    paths = []
    # deal with wildcards
    for path in get_classpath():
        if not path.endswith('*'):
            paths.append(path)
        else:
            paths.extend(glob(path + '.[Jj][Aa][Rr]'))
    return split_char.join(paths)
