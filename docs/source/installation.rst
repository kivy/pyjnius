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

