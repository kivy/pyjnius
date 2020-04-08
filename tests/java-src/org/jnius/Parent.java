package org.jnius;

public class Parent {

	public int doCall(Object o) {
		return 0;
	}

	static public Parent newInstance(){
		return new Parent();
	}

	public int PARENT_FIELD = 0;
}
