# On Android, pyjnius obtains the JVM's JNIEnv from the host process rather than
# creating a JVM itself. Historically this was a *link-time* dependency on SDL2
# (``-lSDL2`` plus a direct reference to ``SDL_AndroidGetJNIEnv``), which
# (a) hard-linked the wheel to one SDL generation and (b) is incompatible with a
# redistributable PEP 738 wheel built with no host app present.
#
# Instead we resolve the env at *runtime*, in order of preference:
#
#   1. SDL_GetAndroidJNIEnv  from libSDL3.so  -- SDL3 (primary; all API levels)
#   2. SDL_AndroidGetJNIEnv  from libSDL2.so  -- SDL2 (primary; all API levels)
#   3. JNI_GetCreatedJavaVMs from libnativehelper.so -- SDL-independent, API 31+
#
# Tiers 1-2 are the primary path and work on every supported API level: a Kivy/SDL
# host loads its SDL library via System.loadLibrary before ``import jnius``, so
# SDL's own JNI_OnLoad has captured the JavaVM, and SDL re-exposes it as the getter
# we resolve here. This is the only viable mechanism for a *dlopen'd* CPython
# extension (see the JNI_OnLoad note below).
#
# How the getter is resolved matters. EMPIRICAL FINDING (p4a SDL2 host, API 32):
# dlsym(RTLD_DEFAULT, "SDL_AndroidGetJNIEnv") returns NULL even though libSDL2.so
# is loaded and exports it -- this .so is a CPython extension dlopen'd from
# site-packages, and the host's System.loadLibrary'd SDL is NOT in its default
# lookup scope. So each tier tries RTLD_DEFAULT first, then dlopen's the library by
# soname (libSDL3.so / libSDL2.so / libnativehelper.so -- all already resident in
# the app linker namespace, so dlopen just returns a handle) and dlsym's that
# handle. dlopen keeps everything runtime-only: no DT_NEEDED on any of them. This
# is the same fix tier 3 needed for libnativehelper (see below).
#
# Tier 3 is a *best-effort* fallback for non-SDL hosts (and cibuildwheel's SDL-less
# testbed). JNI_GetCreatedJavaVMs became a public libnativehelper export only in
# Android 12 / API 31 ("introduced=S"). EMPIRICAL FINDING (cibuildwheel testbed,
# API 35): dlsym(RTLD_DEFAULT, "JNI_GetCreatedJavaVMs") still returns NULL even at
# API 31+, because libnativehelper is not in this extension's default lookup scope.
# The working approach is to dlopen("libnativehelper.so") by soname (permitted for
# apps on API 31+ as a public NDK library) and dlsym the returned handle -- done in
# _resolve_get_created_javavms() below. Verified on-device: autoclass round-trips
# through ART this way (vm.name=Dalvik). On API 24-30 the library is not app-
# accessible, so a non-SDL host there falls through to the clear RuntimeError; that
# is acceptable because the SDL path (tiers 1-2) already covers the real target.
#
# Why NOT JNI_OnLoad(JavaVM*, void*)?  It is the officially-blessed, all-API way to
# receive the JavaVM -- BUT Android only calls it for libraries loaded via Java's
# System.loadLibrary() (ART's LoadNativeLibrary does dlopen + dlsym("JNI_OnLoad")).
# This .so is a CPython extension imported via a plain dlopen(), so ART never calls
# a JNI_OnLoad defined here -- it would be dead code. The host's System.loadLibrary'd
# libs (e.g. SDL) are where JNI_OnLoad legitimately fires; we consume the result of
# theirs via the getters above. A truly SDL-independent, all-API path would require
# the host to hand us the VM explicitly (an explicit runtime-contract setter), not autodetection.
#
# Every symbol here is resolved with dlsym and NONE is linked: the NDK links with
# ``-Wl,--no-undefined``, so a leftover undefined reference (SDL or JNI) would
# fail the link. dlsym keeps the reference dynamic, resolved against whatever the
# host process provides.

cdef extern from "dlfcn.h" nogil:
    void *dlopen(const char *filename, int flag)
    void *dlsym(void *handle, const char *symbol)
    void *RTLD_DEFAULT
    int RTLD_NOW

ctypedef JNIEnv *(*_sdl_get_jnienv_t)() noexcept nogil
ctypedef jint (*_get_created_javavms_t)(JavaVM **, jsize, jsize *) noexcept nogil


cdef void *_resolve_get_created_javavms():
    # JNI_GetCreatedJavaVMs lives in libnativehelper.so (a public NDK library
    # since API 31 / Android 12). Being a *public* export means it can be linked
    # or dlopen'd by soname -- it does NOT mean RTLD_DEFAULT reaches it, because
    # libnativehelper is not in this extension's default lookup scope. Empirically
    # (cibuildwheel testbed, API 35) the RTLD_DEFAULT lookup returns NULL, so we
    # explicitly dlopen the public library by name (allowed for apps on API 31+)
    # and dlsym its handle. dlopen keeps this runtime-only: no DT_NEEDED, so the
    # wheel still loads on hosts/levels where the library is absent.
    cdef void *sym = dlsym(RTLD_DEFAULT, b"JNI_GetCreatedJavaVMs")
    if sym != NULL:
        return sym

    cdef void *handle = dlopen(b"libnativehelper.so", RTLD_NOW)
    if handle != NULL:
        sym = dlsym(handle, b"JNI_GetCreatedJavaVMs")
        if sym != NULL:
            return sym

    # Older/alternate runtimes exported it from libart.so; try that too.
    handle = dlopen(b"libart.so", RTLD_NOW)
    if handle != NULL:
        sym = dlsym(handle, b"JNI_GetCreatedJavaVMs")
        if sym != NULL:
            return sym

    return NULL


cdef void *_resolve_sdl_getter(const char *name, const char *soname):
    # Resolve an SDL JNIEnv getter by symbol name. EMPIRICAL FINDING (p4a SDL2
    # host, API 32): dlsym(RTLD_DEFAULT, "SDL_AndroidGetJNIEnv") returns NULL even
    # though libSDL2.so is resident -- a CPython extension dlopen'd from
    # site-packages does not have the host's System.loadLibrary'd SDL in its
    # default lookup scope. So try RTLD_DEFAULT first (works where SDL is global),
    # then dlopen the SDL soname by name (already loaded in the app linker
    # namespace; dlopen just returns a handle + refcount) and dlsym that handle.
    # dlopen keeps this runtime-only: no DT_NEEDED on any libSDL.
    cdef void *sym = dlsym(RTLD_DEFAULT, name)
    if sym != NULL:
        return sym
    cdef void *handle = dlopen(soname, RTLD_NOW)
    if handle != NULL:
        return dlsym(handle, name)
    return NULL


cdef JNIEnv *_jnienv_from_sdl():
    # SDL3 renamed the getter (SDL_AndroidGetJNIEnv -> SDL_GetAndroidJNIEnv); try
    # SDL3 first, then SDL2. Returns NULL if neither getter is in the process.
    cdef void *sym = _resolve_sdl_getter(b"SDL_GetAndroidJNIEnv", b"libSDL3.so")
    if sym != NULL:
        return (<_sdl_get_jnienv_t>sym)()
    sym = _resolve_sdl_getter(b"SDL_AndroidGetJNIEnv", b"libSDL2.so")
    if sym != NULL:
        return (<_sdl_get_jnienv_t>sym)()
    return NULL


cdef JNIEnv *_jnienv_from_created_vm():
    # SDL-independent, best-effort path. JNI_GetCreatedJavaVMs is a public
    # libnativehelper export only on API 31+ (Android 12); on API 24-30 this
    # dlsym typically returns NULL (the symbol is outside the app linker
    # namespace) and we return NULL so the caller falls through to a clear
    # error. Where it does resolve, it yields the process' existing JavaVM and
    # we attach the current thread to obtain its JNIEnv. Returns NULL if the
    # symbol is absent, no VM has been created, or the attach fails.
    cdef void *sym = _resolve_get_created_javavms()
    if sym == NULL:
        return NULL

    cdef JavaVM *vm = NULL
    cdef jsize n_vms = 0
    if (<_get_created_javavms_t>sym)(&vm, 1, &n_vms) != 0 or n_vms < 1 or vm == NULL:
        return NULL

    cdef void *env = NULL
    if vm[0].AttachCurrentThread(vm, &env, NULL) != 0:
        return NULL
    return <JNIEnv*>env


cdef JNIEnv *get_platform_jnienv() except NULL:
    cdef JNIEnv *env = _jnienv_from_sdl()
    if env == NULL:
        env = _jnienv_from_created_vm()

    if env != NULL:
        return env

    raise RuntimeError(
        "pyjnius (Android) could not obtain a JNIEnv: no SDL JNIEnv getter "
        "(SDL_GetAndroidJNIEnv / SDL_AndroidGetJNIEnv) and no in-process JVM "
        "(JNI_GetCreatedJavaVMs) were found in the process. The host must "
        "provide an in-process JVM before the first 'import jnius' -- e.g. a "
        "Kivy/SDL app loads its SDL library (libSDL3.so or libSDL2.so) with "
        "global symbol visibility, which exposes the SDL getter."
    )
