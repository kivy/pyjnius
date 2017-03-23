.. _installation:

Installation
============

Pyjnius depends on `Cython <http://cython.org/>`_ and `Java
<http://www.oracle.com/javase>`_.


Installation on the Desktop
---------------------------

You need the Java JDK and JRE installed (openjdk will do), and Cython. Then,
just type::

    sudo python setup.py install

If you want to compile the extension within the directory for any development,
just type::

    make

You can run the tests suite to make sure everything is running right::

    make tests


Installation for Android
------------------------

If you use `Python for android <http://github.com/kivy/python-for-android>`,
you just need to compile a distribution with the pyjnius module::

    ./distribute.sh -m 'pyjnius kivy'


Installation for Windows
------------------------

Python and pip must be installed and present in PATH.


1. Download and install JDK and JRE:
    http://www.oracle.com/technetwork/java/javase/downloads/index.html

2. Edit your system and environment variables (use the appropriate Java version):
    Add to Environment Variables:
        * ``JDK_HOME``: C:\\Program Files\\Java\\jdk1.7.0_79\\
        * ``PATH``: C:\\Program Files\\Java\\jdk1.7.0_79\\jre\\bin\\server\\
    Add to System Variables:
        * ``PATH``: C:\\Program Files\\Java\\jdk1.7.0_79\\bin\\`

3. Download and install Microsoft Visual C++ Compiler for Python 2.7:
    http://aka.ms/vcpython27

4. Update pip and setuptools::

    python -m pip install --upgrade pip setuptools

5. Install Cython::

    python -m pip install --upgrade Cython

6. Install Pyjnius::

    pip install pyjnius
