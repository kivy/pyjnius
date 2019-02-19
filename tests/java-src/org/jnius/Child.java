package org.jnius;

import org.jnius.Parent;

public class Child extends Parent {
	static public Child newInstance(){
		return new Child();
	}
}
