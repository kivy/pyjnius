package jnius;
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;

public class NativeInvocationHandler implements InvocationHandler {
	public NativeInvocationHandler(long ptr) {
		this.ptr = ptr;
	}

	public Object invoke(Object proxy, Method method, Object[] args) {
		/**
		if ( method.getName() == "toString" ) {
			System.out.println("+ java:invoke toString.");
			return "<proxy>";
		}
		/**/
		System.out.print("+ java:invoke(<proxy>, ");
		// don't call it, or recursive lookup/proxy will go!
		//System.out.print(proxy);
		//System.out.print(", ");
		System.out.print(method);
		System.out.print(", ");
		System.out.print(args);
		System.out.println(")");
		System.out.println(method.getName());
		System.out.println(method.getParameterTypes());
		System.out.print("+ java:call native invoke0() >>>");
		Object ret = invoke0(proxy, method, args);
		System.out.println("+ java:call native invoke0() <<<");
		System.out.print("+ java:invoke returned ");
		System.out.println(ret);
		return ret;
	}

	native Object invoke0(Object proxy, Method method, Object[] args);

	private long ptr;
}
