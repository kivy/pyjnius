.. _android-wheel:

Android wheels
==============

PyJNIus can be published as a prebuilt `PEP 738 <https://peps.python.org/pep-0738/>`_
Android wheel (``android_*`` tags), so an Android packager can ``pip install``
it instead of compiling from source per app. The wheel is **SDL-agnostic** and
**Java-free**: it resolves the JVM ``JNIEnv`` at runtime and ships no Java. In
return, the host application must satisfy a small runtime contract (below).

.. note::
   This describes the *redistributable* wheel. On desktop, PyJNIus still starts
   its own JVM and bundles the compiled ``NativeInvocationHandler.class`` as
   before; nothing here changes desktop behavior.


The runtime contract
--------------------

The wheel does **not** create a JVM on Android; it attaches to the one the host
process already has. A conforming host must provide:

1. **An in-process JVM discoverable at import.** The ``JNIEnv`` is resolved at
   the first ``import jnius`` in this order:

   * ``SDL_GetAndroidJNIEnv`` from ``libSDL3.so`` (SDL3), else
   * ``SDL_AndroidGetJNIEnv`` from ``libSDL2.so`` (SDL2), else
   * ``JNI_GetCreatedJavaVMs`` from ``libnativehelper.so`` (SDL-independent,
     **API 31+ only**) + ``AttachCurrentThread``.

   For an SDL host, its SDL library must be **loaded before the first**
   ``import jnius`` (a Kivy/SDL app loads SDL at startup, which captures the
   ``JavaVM`` via SDL's own ``JNI_OnLoad``). Each tier tries
   ``dlsym(RTLD_DEFAULT, ...)`` first, then ``dlopen``\ s the library by soname
   and resolves the symbol from that handle -- a CPython extension imported via
   ``dlopen`` does not have the host's ``System.loadLibrary``\ 'd SDL in its
   default lookup scope. No ``DT_NEEDED`` on any ``libSDL``/``libnativehelper``
   is created, so the wheel loads regardless of which (if any) SDL is present.

2. **The Java glue on the app's dex classpath.** PyJNIus's
   *Python-implements-a-Java-interface* feature
   (``PythonJavaClass``/``@java_method``) needs the class
   ``org.jnius.NativeInvocationHandler``. A ``.whl`` carries no ``.dex`` and a
   class in ``site-packages`` is **not** on ART's classpath, so the wheel does
   not and cannot deliver it. The packager (bootstrap/build system) must compile
   and dex ``org.jnius.NativeInvocationHandler`` into the APK. Plain ``autoclass``
   and method calls need no glue; only proxies do.

   .. warning::
      **Matched-pair coupling.** The wheel's native ``invoke0`` contract (bound
      at runtime via ``RegisterNatives``) and the packager's copy of
      ``NativeInvocationHandler.java`` must be updated together. Nothing enforces
      this once the glue is out of the wheel -- a mismatch surfaces as a
      ``ClassNotFound``/``NoSuchMethod`` at first proxy creation. The canonical
      source lives in the PyJNIus repository at
      ``jnius/src/org/jnius/NativeInvocationHandler.java``.

If no JVM/glue is found, the first ``import jnius`` raises a clear
``RuntimeError`` naming the missing getter, rather than a cryptic dlopen/symbol
failure.


Building the wheel
------------------

Build on a Linux ``x86_64`` (WSL2 counts) or macOS host with an Android SDK;
`cibuildwheel <https://cibuildwheel.pypa.io/en/stable/platforms/#android>`_
drives the NDK via ``sdkmanager``. The pinned toolchain lives in
``[tool.cibuildwheel.android]`` in ``pyproject.toml``.

.. code:: bash

    # 1. Android compiles a *pre-generated* jnius.c (Cython is build-only and not
    #    needed on the target). config.pxi selects the android include branch.
    printf "DEF JNIUS_PLATFORM = 'android'\n" > jnius/config.pxi
    cython -3 jnius/jnius.pyx -o jnius/jnius.c

    # 2. Build from a CLEAN tree. `python -m build --no-isolation` reuses
    #    build/lib.android-*; a stale one from an earlier build re-injects the
    #    Java payload and breaks the Java-free guarantee. A fresh checkout (CI) is
    #    already clean.
    rm -rf build

    # 3. arm64_v8a ships to devices; x86_64 is the testability ABI (cibuildwheel's
    #    emulator testbed only runs the build-host arch).
    cibuildwheel --only cp314-android_arm64_v8a --output-dir wheelhouse
    cibuildwheel --only cp314-android_x86_64    --output-dir wheelhouse

The frontend must be ``build``/``uv`` (Android does not support the ``pip``
frontend); this is set in ``pyproject.toml``. CPython 3.15 (pre-release until
Oct 2026) additionally needs ``--enable cpython-prerelease``.

**16 KB page alignment.** Android 15/16 requires native ``.so``\ s to have
16 KB-aligned LOAD segments. The build pins
``LDFLAGS = "-Wl,-z,max-page-size=16384"`` in ``[tool.cibuildwheel.android]`` so
the wheel is 16 KB-aligned independent of the NDK's default. This aligns only
PyJNIus's ``.so`` -- the packager is responsible for aligning the bootstrap libs
(SDL, libpython, ...) and for 16 KB zip-aligning the final APK.


Verifying a built wheel
----------------------

.. code:: bash

    # unzip the wheel, then, with the NDK's llvm-readelf:
    llvm-readelf -d jnius/jnius*.so | grep NEEDED     # no libSDL / libnativehelper / libart
    llvm-readelf -l jnius/jnius*.so | grep LOAD       # Align column == 0x4000 (16 KB)
    llvm-readelf --dyn-syms jnius/jnius*.so | grep -E 'dlopen|dlsym'   # runtime-resolved

The wheel should contain only the ``.so`` and the Python modules -- no
``src/org``, ``.java`` or ``.class``.
