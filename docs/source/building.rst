.. _building:

Building PYJNIus
================

Building PyJNIus depends on `Cython <http://cython.org/>`_ and the `Java
<http://www.oracle.com/javase>`_ Development Kit (includes the Java Runtime
Environment).


Building on GNU/Linux distributions
-----------------------------------

You need the GNU Compiler Collection (GCC), the JDK installed (openjdk
will do), and Cython. Then, just type::

    sudo python setup.py install

If you want to compile the extension within the directory for any development,
just type::

    make

You can run the tests suite to make sure everything is running right::

    make tests


Building on Windows
-------------------

Python and pip must be installed and present in the ``PATH`` environment variable.


1. Download and install the JDK containing the JRE:

   http://www.oracle.com/technetwork/java/javase/downloads/index.html

2. Edit your system and environment variables (use the appropriate Java bitness
   and version in the paths):

    Add to your `Environment Variables
    <https://en.wikipedia.org/wiki/Environment_variable>`_:

    * ``JAVA_HOME``: C:\\Program Files\\Java\\jdk1.7.0_79\\bin
    * ``PATH``: C:\\Program Files\\Java\\jdk1.7.0_79\\jre\\bin\\server
      contains the ``jvm.dll`` necessary for importing and using PyJNIus.

      .. note::
         set PATH=%PATH%;C:\\Program Files\\Java\\jdk1.7.0_79\\jre\\bin\\server

    Add to System Variables or have it present in your ``PATH``:
        * ``PATH``: C:\\Program Files\\Java\\jdk1.7.0_79\\bin`

3. Download and install the C compiler:

   a) Microsoft Visual C++ Compiler for Python 2.7:

      http://aka.ms/vcpython27

   b) MinGWPy for Python 2.7:

      https://anaconda.org/carlkl/mingwpy

   c) Microsoft Visual C++ Build Tools (command-line tools subset of Visual
      Studio) for Python 3.5 and 3.6:

      https://visualstudio.microsoft.com/downloads/

   For other versions see Python's `Windows Compilers wiki
   <https://wiki.python.org/moin/WindowsCompilers>`_.

4. Update `pip <https://pip.pypa.io/en/stable/installing>`_ and setuptools::

      python -m pip install --upgrade pip setuptools

5. Install Cython::

       python -m pip install --upgrade cython

6. Install Pyjnius::

       pip install pyjnius

   .. note::
       In case of MinGWPy's GCC returning a ``CreateProcess failed: 5`` error
       you need to run the command prompt with elevated permissions, so that
       the compiler can access the JDK in ``C:\Program Files\Java\jdkx.y.z_b``
       or ``C:\Program Files (x86)\Java\jdkx.y.z_b``.


Building for macOS
------------------

Python and pip must be installed and present in the ``PATH`` environment variable.


1. Download and install the JDK containing the JRE:

   http://www.oracle.com/technetwork/java/javase/downloads/index.html

2. Edit your system and environment variables (use the appropriate Java bitness
   and version in the paths):

    Add to your `Environment Variables
    <https://en.wikipedia.org/wiki/Environment_variable>`_:

    * ``export JAVA_HOME=/usr/libexec/java_home``

3. Install Xcode command-line tools.

4. Update `pip <https://pip.pypa.io/en/stable/installing>`_ and setuptools::

      python -m pip install --upgrade pip setuptools

5. Install Cython::

       python -m pip install --upgrade cython

6. Install Pyjnius::

       pip install pyjnius

