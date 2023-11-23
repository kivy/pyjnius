.. _building:

Building PYJNIus
================

Building PyJNIus is necessary for development purposes, or if there is no 
pre-built binary for your particular platform. 

Like installation of PyJNIus, building PyJNIus requires a  `Java
<https://www.oracle.com/java/technologies/downloads/>`_ Development Kit 
to be installed.

Apart from the JDK, the building requirements for each platform are as follows:

 - Linux: the GNU Compiler Collection (GCC).
 - Windows Microsoft Visual C++ Build Tools (command-line tools subset of Visual
   Studio) can be obtained from https://visualstudio.microsoft.com/downloads/. 
   For more information or options, see Python's `Windows Compilers wiki
   <https://wiki.python.org/moin/WindowsCompilers>`_.
 - macOS: `Xcode command-line tools <https://mac.install.guide/commandlinetools/index.html>`_.

In all cases, PyJNIus can be *built* and installed using::

     pip install .

This installs Cython (as specified in the 
`pyproject.toml <https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/>`_) 
in a Python build environment. On all platforms, if PyJNIus cannot find your JDK, you can set 
the `JAVA_HOME` shell environment variable (this is often needed on Windows).

If you want to compile the PyJNIus extension within the directory for any development,
just type::

    make

You can run the tests suite to make sure everything is running right::

    make tests

In these cases, you may need to have `Cython <https://pypi.org/project/Cython/>`_ 
and `pytest <https://pypi.org/project/pytest/>`_ installed in the current Python environment.