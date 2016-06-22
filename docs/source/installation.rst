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

1. Download and install JDK and JRE (if not installed): 
  * http://www.oracle.com/technetwork/java/javase/downloads/index.html
  
2. Edit your system and environment variables (use your appropriate your java version):
  
  1. Add to Environment Variables:
    * ``JDK_HOME``: C:\\Program Files\\Java\\jdk1.7.0_79\\
    * ``PATH``: C:\\Program Files\\Java\\jdk1.7.0_79\\jre\\bin\\server\\
  2. Add to System Variables:
    * ``PATH``: C:\\Program Files\Java\jdk1.7.0_79\bin\`

3.	Install pip (if not installed):
    - https://pip.pypa.io/en/latest/installing/

4.	Download and install Cython (if not installed):
  1. Install wheel: 
    * ``pip install wheel``
  2. Install Cython:
    1. Download Cython for Windows: 
      * http://www.lfd.uci.edu/~gohlke/pythonlibs/#cython
    2. Install Cython (use your appropriate filename):
      * ``pip install Cython-0.24-cp35-cp35m-win_amd64.whl``

5.	Download and install  Microsoft Visual C++ Compiler for Python 2.7:
  1. http://aka.ms/vcpython27
    Python modules can be part written in C (typically for speed).  If you try to install such a package with ``pip`` (or ``setup.py``), it has to compile that C/C++ from source. `[Reference] <http://stackoverflow.com/questions/2817869/error-unable-to-find-vcvarsall-bat/26127562#26127562>`_
  2. Install ``setuptools`` for the compiler to work:  
    * https://pypi.python.org/pypi/setuptools#windows-simplified

6.	Download and install the pyjnius source:
    - https://github.com/kivy/pyjnius
    - ``python setup.py install``
