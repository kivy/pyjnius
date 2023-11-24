.. _installation:

Installation
============

PyJNIus has pre-compiled binaries on PyPi for recent Python versions on Linux,
macOS and Windows.

On each platform::

   pip install pyjnius

should successfully install the package.

If there is no pre-compiled binary available, pip install will aim to compile
a binary on your operating system. For more information see the :ref:`building` 
documentation.

You will need the Java JDK installed (`OpenJDK <https://openjdk.org/>`_ is fine).
PyJNIus searches for Java in the usual places on each operating system. If PyJNIus 
cannot find Java, set the `JAVA_HOME` environment variable (this is often needed 
`on Windows <https://www.baeldung.com/java-home-on-windows-7-8-10-mac-os-x-linux#windows>`_).

Installation for Android
------------------------

To use pyjnius in an Android app, you must include it in your compiled
Python distribution. This is done automatically if you build a `Kivy
<https://kivy.org/#home>`__ app, but you can also add it to your
requirements explicitly as follows.

If you use `buildozer
<https://buildozer.readthedocs.io/en/latest/>`__, add pyjnius to your
requirements in buildozer.spec::

  requirements = pyjnius

If you use `python-for-android
<http://python-for-android.readthedocs.io/en/latest/>`__ directly, add
pyjnius to the requirements argument when creating a dist or apk::

  p4a apk --requirements=pyjnius


Installation for Conda
----------------------

Similar to PIP there is a package manager for
`Anaconda <https://www.anaconda.com/what-is-anaconda/>` called Conda.
An unofficial compiled distributions of PyJNIus for Conda supported
platforms you can find at https://anaconda.org/conda-forge/pyjnius.

You can install ``pyjnius`` with this command::

    conda install -c conda-forge pyjnius

Or if you want a specific package label e.g. ``gcc7``::

    conda install -c conda-forge/label/gcc7 pyjnius
