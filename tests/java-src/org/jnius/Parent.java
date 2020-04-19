package org.jnius;

public class Parent {

	public static int STATIC_PARENT_FIELD = 1;

	public int doCall(Object o) {
		return 0;
	}

	public int getParentStaticField() {
		return STATIC_PARENT_FIELD;
	}

	public static int StaticGetParentStaticField() {
		return STATIC_PARENT_FIELD;
	}

	public int getParentField() {
		return PARENT_FIELD;
	}

	static public Parent newInstance(){
		return new Parent();
	}

	public int PARENT_FIELD = 0;
}
