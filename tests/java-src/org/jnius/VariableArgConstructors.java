package org.jnius;

public class VariableArgConstructors {
  public int constructorUsed;

  public VariableArgConstructors(int arg1, String arg2, int arg3, Object arg4, int... arg5) {
    constructorUsed = 1;
  }

  public VariableArgConstructors(int arg1, String arg2, Object arg3, int... arg4) {
    constructorUsed = 2;
  }

}