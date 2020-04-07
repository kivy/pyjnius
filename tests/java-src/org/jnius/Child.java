package org.jnius;

import org.jnius.Parent;

public class Child extends Parent {

	public int CHILD_FIELD = 1;

	public int doCall(int child) {
		return 1;
	}

	static public Child newInstance(){
		return new Child();
	}
}
