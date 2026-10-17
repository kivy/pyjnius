.. _building:

Building PyJNIus
================

Building PyJNIus is necessary for development purposes, or if there is no 
pre-built binary for your particular platform. 

Building PyJNIus requires a  `Java Development Kit
<https://www.oracle.com/java/technologies/downloads/>`_  (JDK)
to be installed (NB: installing pre-built wheels requires only a JRE).

Apart from the JDK, the build requirements for each platform are as follows:

 - Linux: the `GNU Compiler Collection <https://gcc.gnu.org/>`_ (GCC), e.g. using 
   `apt-get install build-essentials` on Debian-based distributions.
 - Windows: `Microsoft Visual C++ Build Tools <https://visualstudio.microsoft.com/downloads/>`_ 
   (the command-line tools subset of Visual Studio). 
   For more information or options, see Python's `Windows Compilers wiki
   <https://wiki.python.org/moin/WindowsCompilers>`_.
 - macOS: `Xcode command-line tools <https://mac.install.guide/commandlinetools/index.html>`_.

In all cases, after checking out PyJNIus from GitHub, it can be *built* and installed using::

     pip install .

This installs `Cython <https://cython.org/>`_ (as specified in the 
`pyproject.toml <https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/>`_) 
in a Python build environment. On all platforms, if PyJNIus cannot find your JDK, you can set 
the `JAVA_HOME` environment variable (this is often needed on Windows).

If you want to compile the PyJNIus extension within the directory for any development,
just type::

    make

You can run the tests suite to make sure everything is running right::

    make tests

In these cases, you may need to have `Cython <https://pypi.org/project/Cython/>`_ 
and `pytest <https://pypi.org/project/pytest/>`_ installed in the current Python environment.

Desktop wheel CI
----------------

For build-tool changes, include ``[build wheel]`` in the PR title before opening
the PR or pushing another commit to exercise the release-shaped builds and tests.
The existing pytest suite runs against the installed wheel, with only Java test
fixtures compiled separately so the packaged helpers are used. Wheel-test
failures block tag releases.

One Linux x86_64 / Python 3.14 job runs the built wheel on Java 8, independently
of the build JDK; the other wheel jobs use Java 17. This is a representative
backwards-compatibility check for toolchain bumps, rather than an exhaustive
Python/JVM/platform guarantee. User-reported incompatibilities can be covered
by targeted regression tests.
