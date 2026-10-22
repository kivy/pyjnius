.. _installation:

Installation
============

PyJNIus has pre-compiled binaries on PyPI for recent Python versions on Linux,
macOS and Windows.

On each platform::

   pip install pyjnius

should successfully install the package.

If there is no pre-compiled binary available, pip install will aim to compile
a binary on your operating system. For more information see the :ref:`building` 
documentation.

You will need the Java JRE installed (`OpenJDK <https://openjdk.org/>`_ is fine).

PyJNIus first uses a nonempty ``JAVA_HOME``, ``JDK_HOME``, or ``JRE_HOME``,
in that order.

On Windows, one of these variables must be set; PyJNIus does not search
``PATH`` for Java. See the `Windows JAVA_HOME configuration guide
<https://www.baeldung.com/java-home-on-windows-7-8-10-mac-os-x-linux#windows>`_.

If no home is selected, macOS uses the system ``java_home`` helper. On
other Unix-like systems, automatic discovery prefers ``javac`` on
``PATH``, then ``java``, then the usual default Java directories. If
PyJNIus cannot find Java, set the ``JAVA_HOME`` environment variable.

A runtime-only installation is sufficient to use a prebuilt wheel;
building PyJNIus from source requires a JDK.

Installation from source
------------------------

To install PyJNIus from the `GitHub repository <https://github.com/kivy/pyjnius>`_::

    git clone https://github.com/kivy/pyjnius.git
    cd pyjnius
    pip install .

See :ref:`building` for build requirements and development instructions.

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
<https://python-for-android.readthedocs.io/en/latest/>`__ directly, add
pyjnius to the requirements argument when creating a dist or apk::

  p4a apk --requirements=pyjnius


Installation for Conda
----------------------

An unofficial pre-compiled distribution of PyJNIus is available for
`Conda <https://docs.conda.io/en/latest/>`_ on supported platforms through
`conda-forge <https://anaconda.org/conda-forge/pyjnius>`_.

You can install ``pyjnius`` with this command::

    conda install -c conda-forge pyjnius

Or if you want a specific package label e.g. ``gcc7``::

    conda install -c conda-forge/label/gcc7 pyjnius
