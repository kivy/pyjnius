
cdef JNIEnv *env_current = NULL
cdef JNIEnv *env_stacks[256]
cdef int env_stack = -1

cdef JNIEnv *get_jnienv():
    global env_stacks, env_stack, env_current
    # first call, init.
    if env_stack == -1:
        env_stacks[0] = env_current = get_platform_jnienv()
        env_stack = 0
    return env_current

cdef void push_jnienv(JNIEnv *env) nogil:
    global env_stacks, env_stack, env_current
    if env_stack == 255:
        with gil:
            print('ERROR: Jnius cannot push JNI env, too many entries')
        return
    env_stack += 1
    env_stacks[env_stack] = env_current = env

cdef void pop_jnienv() nogil:
    global env_stacks, env_stack, env_current
    if env_stack == 0:
        with gil:
            print('ERROR: Jnius cannot pop JNI env, already at 0')
        return
    env_stacks[env_stack] = NULL
    env_stack -= 1
    env_current = env_stacks[env_stack]

