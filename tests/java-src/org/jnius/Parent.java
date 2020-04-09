package org.jnius;

public class Parent {

	public static int STATIC_PARENT_FIELD = 1;

	public int doCall(Object o) {
		return 0;
	}

	static public Parent newInstance(){
		return new Parent();
	}

	public int PARENT_FIELD = 0;
}
