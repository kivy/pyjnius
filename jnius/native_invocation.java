import java.lang.reflect.InvocationHandler;

public class NativeInvocationHandler implements InvocationHandler {
	public NativeInvocationHandler(long ptr) {
		this.ptr = ptr;
	}

	Object invoke(Object proxy, Method method, Object[] args) {
		return invoke0(proxy, method, args);
	}

	native private Object invoke0(Object proxy, Method method, Object[] args);

	private long ptr;
}

class NativeInvocationHandler {
	public:
		virtual ~NativeInvocationHandler();
		virtual jobject Invoke(JNIEnv *, jobject method, jobjectArray args) = 0;
};
