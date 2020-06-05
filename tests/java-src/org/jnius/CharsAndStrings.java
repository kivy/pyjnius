package org.jnius;

import java.lang.String;

public class CharsAndStrings {
  
  public char testChar1;
  public char testChar2;
  public char testChar3;
  public String testString1;
  public String testString2;
  public String testString3;
  
  static public char testStaticChar1 = 'a';
  static public char testStaticChar2 = 'ä';
  static public char testStaticChar3 = '☺';
  static public String testStaticString1 = "hello world";
  static public String testStaticString2 = "umlauts: äöü";
  static public String testStaticString3 = "happy face: ☺";

  public char[] testCharArray1;
  public char[] testCharArray2;
  static public char[] testStaticCharArray1 = new char[]{'a', 'b', 'c'};
  static public char[] testStaticCharArray2 = new char[]{'a', 'ä', '☺'};
  static public String testStringDefNull = null;
  static public int testInt = 0;

  public CharsAndStrings() {
    this.testChar1 = 'a';
    this.testChar2 = 'ä';
    this.testChar3 = '☺';

    this.testString1 = "hello world";
    this.testString2 = "umlauts: äöü";
    this.testString3 = "happy face: ☺";

    testCharArray1 = new char[]{'a', 'b', 'c'};
    testCharArray2 = new char[]{'a', 'ä', '☺'};
  }

  public char testChar(int i, char testChar) {
    if (i == 1) {
      assert this.testChar1 == testChar;
      return this.testChar1;
    } else if (i == 2) {
      assert this.testChar2 == testChar;
      return this.testChar2;
    } else {
      assert this.testChar3 == testChar;
      return this.testChar3;
    }
  }

  static public char testStaticChar(int i, char testChar) {
    if (i == 1) {
      assert CharsAndStrings.testStaticChar1 == testChar;
      return CharsAndStrings.testStaticChar1;
    } else if (i == 2) {
      assert CharsAndStrings.testStaticChar2 == testChar;
      return CharsAndStrings.testStaticChar2;
    } else {
      assert CharsAndStrings.testStaticChar3 == testChar;
      return CharsAndStrings.testStaticChar3;
    }
  }

  public String testString(int i, String testString) {
    if (i == 1) {
      assert this.testString1.equals(testString);
      return this.testString1;
    } else if (i == 2) {
      assert this.testString2.equals(testString);
      return this.testString2;
    } else {
      assert this.testString3.equals(testString);
      return this.testString3;
    }
  }

  static public String testStaticString(int i, String testString) {
    if (i == 1) {
      assert CharsAndStrings.testStaticString1.equals(testString);
      return CharsAndStrings.testStaticString1;
    } else if (i == 2) {
      assert CharsAndStrings.testStaticString2.equals(testString);
      return CharsAndStrings.testStaticString2;
    } else {
      assert CharsAndStrings.testStaticString3.equals(testString);
      return CharsAndStrings.testStaticString3;
    }
  }

  public char[] testCharArray(int i) {
    if (i == 1) {
      return testCharArray1;
    } else {
      return testCharArray2;
    }
  }

  static public char[] testStaticCharArray(int i) {
    if (i == 1) {
      return testStaticCharArray1;
    } else {
      return testStaticCharArray2;
    }
  }

  static public void setString(String ignore, String value) {
    testStringDefNull  = value;
  }
  
  static public void setInt(String ignore, int value) {
    testInt  = value;
  } 
}
