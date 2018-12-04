.. _packaging:

Packaging
=========

For Packaging we use `PyInstaller <http://www.pyinstaller.org/>`_ and with
these simple steps we will create a simple executable containing PyJNIus
that prints the path of currently used Java. These steps assume you have
a supported version of Python for PyJNIus and PyInstaller available together
with Java installed (necessary for running the application).

main.py
-------

.. code:: python

    from jnius import autoclass

    if __name__ == '__main__':
        print(autoclass('java.lang.System').getProperty('java.home'))

This will be our ``main.py`` file. You can now call PyInstaller to create
a basic ``.spec`` file which contains basic instructions for PyInstaller with::

    pyinstaller main.py

main.spec
---------

The created ``.spec`` file might look like this::

    # -*- mode: python -*-
    
    block_cipher = None
    
    
    a = Analysis(
        ['main.py'],
        pathex=['<some path to main.py folder>'],
        binaries=None,
        datas=None,
        hiddenimports=[],
        hookspath=[],
        runtime_hooks=[],
        excludes=[],
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        cipher=block_cipher
    )
    
    pyz = PYZ(
        a.pure,
        a.zipped_data,
        cipher=block_cipher
    )
    
    exe = EXE(
        pyz,
        a.scripts,
        exclude_binaries=True,
        name='main',
        debug=False,
        strip=False,
        upx=True,
        console=True
    )
    
    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        name='main'
    )

Notice the ``Analysis`` section, it contains details for what Python related
files to collect e.g. the ``main.py`` file. For PyJNIus to work you need to
include the ``jnius_config`` module to the ``hiddenimports`` list, otherwise
you will get a ``ImportError: No module named jnius_config``::

    ...

    a = Analysis(
        ['main.py'],
        pathex=['<some path to main.py folder>'],
        binaries=None,
        datas=None,
        hiddenimports=['jnius_config'],
        hookspath=[],
        runtime_hooks=[],
        excludes=[],
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        cipher=block_cipher
    )

    ...

After the ``.spec`` file is ready, in our case it's by default called by the
name of the ``.py`` file, we need to direct PyInstaller to use that file::

    pyinstaller main.spec

This will create a folder with all required ``.dll`` and ``.pyd`` or ``.so``
shared libraries and other necessary files for our application and for Python
itself.

Running
-------

We have the application ready, but the "problem" is PyJNIus doesn't detect
any installed Java on your computer (yet). Therefore if you try to run the
application, it'll crash with a ``ImportError: DLL load failed: ...``.
For this simple example if you can see ``jnius.jnius.pyd`` or
``jnius.jnius.so`` in the final folder with ``main.exe`` (or just ``main``),
the error indicates that the application could not find Java Virtual Machine.

The Java Virtual Machine is in simple terms said another necessary shared
library your application needs to load (``jvm.dll`` or ``libjvm.so``).

On Windows this file might be in a folder similar to this::

    C:\Program Files\Java\jdk1.7.0_79\jre\bin\server

and you need to include the folder to the system ``PATH`` environment variable
with this command::

    set PATH=%PATH%;C:\\Program Files\\Java\\jdk1.7.0_79\\jre\\bin\\server

After the ``jvm.dll`` or ``libjvm.so`` becomes available, you can safely
try to run your application::

    main.exe

and you should get an output similar to this::

    C:\Program Files\Java\jdk1.7.0_79\jre
