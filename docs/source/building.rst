.. _building:

Building PyJNIus
================

Building PyJNIus is necessary for development purposes, or if there is no 
pre-built binary for your particular platform. 

Like installation of PyJNIus, building PyJNIus requires a  `Java Development Kit
<https://www.oracle.com/java/technologies/downloads/>`_  (JDK)
to be installed.

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