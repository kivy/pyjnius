package org.jnius;

import java.lang.String;

public class BasicsTest {
	static public boolean methodStaticZ() { return true; };
	static public byte methodStaticB() { return 127; };
	static public char methodStaticC() { return 'k'; };
	static public short methodStaticS() { return 32767; };
	static public int methodStaticI() { return 2147483467; };
	static public long methodStaticJ() { return 2147483467; };
	static public float methodStaticF() { return 1.23456789f; };
	static public double methodStaticD() { return 1.23456789; };
	static public String methodStaticString() { return new String("helloworld"); }

	public boolean methodZ() { return true; };
	public byte methodB() { return 127; };
	public char methodC() { return 'k'; };
	public short methodS() { return 32767; };
	public int methodI() { return 2147483467; };
	public long methodJ() { return 2147483467; };
	public float methodF() { return 1.23456789f; };
	public double methodD() { return 1.23456789; };
	public String methodString() { return new String("helloworld"); }
	public void methodException(int depth) throws IllegalArgumentException {
		if (depth == 0) throw new IllegalArgumentException("helloworld");
		else methodException(depth -1);
	}
	public void methodExceptionChained() throws IllegalArgumentException {
		try {
			methodException(5);
		} catch (IllegalArgumentException e) {
			throw new IllegalArgumentException("helloworld2", e);
		}
	}

	static public boolean fieldStaticZ = true;
	static public byte fieldStaticB = 127;
	static public char fieldStaticC = 'k';
	static public short fieldStaticS = 32767;
	static public int fieldStaticI = 2147483467;
	static public long fieldStaticJ = 2147483467;
	static public float fieldStaticF = 1.23456789f;
	static public double fieldStaticD = 1.23456789;
	static public String fieldStaticString = new String("helloworld");

	public boolean fieldZ = true;
	public byte fieldB = 127;
	public char fieldC = 'k';
	public short fieldS = 32767;
	public int fieldI = 2147483467;
	public long fieldJ = 2147483467;
	public float fieldF = 1.23456789f;
	public double fieldD = 1.23456789;
	public String fieldString = new String("helloworld");

	public boolean fieldSetZ;
	public byte fieldSetB;
	public char fieldSetC;
	public short fieldSetS;
	public int fieldSetI;
	public long fieldSetJ;
	public float fieldSetF;
	public double fieldSetD;
	public String fieldSetString;

	// Floating-point comparison epsilon
	private final static double EPSILON = 1E-6;

    public BasicsTest() {}
    public BasicsTest(byte fieldBVal) {
        fieldB = fieldBVal;
    }

	public boolean[] methodArrayZ() {
		boolean[] x = new boolean[3];
		x[0] = x[1] = x[2] = true;
		return x;
	};
	public byte[] methodArrayB() {
		byte[] x = new byte[3];
		x[0] = x[1] = x[2] = 127;
		return x;
	};
	public char[] methodArrayC() {
		char[] x = new char[3];
		x[0] = x[1] = x[2] = 'k';
		return x;
	};
	public short[] methodArrayS() {
		short[] x = new short[3];
		x[0] = x[1] = x[2] = 32767;
		return x;
	};
	public int[] methodArrayI() {
		int[] x = new int[3];
		x[0] = x[1] = x[2] = 2147483467;
		return x;
	};
	public long[] methodArrayJ() {
		long[] x = new long[3];
		x[0] = x[1] = x[2] = 2147483467;
		return x;
	};
	public float[] methodArrayF() {
		float[] x = new float[3];
		x[0] = x[1] = x[2] = 1.23456789f;
		return x;
	};
	public double[] methodArrayD() {
		double[] x = new double[3];
		x[0] = x[1] = x[2] = 1.23456789;
		return x;
	};
	public String[] methodArrayString() {
		String[] x = new String[3];
		x[0] = x[1] = x[2] = new String("helloworld");
		return x;
	};


	public boolean methodParamsZBCSIJFD(boolean x1, byte x2, char x3, short x4,
			int x5, long x6, float x7, double x8) {
		return (x1 == true && x2 == 127 && x3 == 'k' && x4 == 32767 &&
				x5 == 2147483467 && x6 == 2147483467 &&
				(Math.abs(x7 - 1.23456789f) < EPSILON) &&
				(Math.abs(x8 - 1.23456789) < EPSILON));
	}

	public boolean methodParamsString(String s) {
		return (s.equals("helloworld"));
	}

	public boolean methodParamsArrayI(int[] x) {
		if (x.length != 3)
			return false;
		return (x[0] == 1 && x[1] == 2 && x[2] == 3);
	}

	public boolean methodParamsArrayString(String[] x) {
		if (x.length != 2)
			return false;
		return (x[0].equals("hello") && x[1].equals("world"));
	}

	public boolean methodParamsObject(Object x) {
		return true;
	}

	public Object methodReturnStrings() {
		String[] hello_world = new String[2];
		hello_world[0] = "Hello";
		hello_world[1] = "world";
		return hello_world;
	}

	public Object methodReturnIntegers() {
		int[] integers = new int[2];
		integers[0] = 1;
		integers[1] = 2;
		return integers;
	}

	public boolean methodParamsArrayByte(byte[] x) {
		if (x.length != 3)
			return false;
		return (x[0] == 127 && x[1] == 127 && x[2] == 127);
	}

	public void fillByteArray(byte[] x) {
		if (x.length != 3)
			return;
		x[0] = 127;
		x[1] = 1;
		x[2] = -127;
	}

	public boolean testFieldSetZ() {
		return (fieldSetZ == true);
	}

	public boolean testFieldSetB() {
		return (fieldSetB == 127);
	}

	public boolean testFieldSetC() {
		return (fieldSetC == 'k');
	}

	public boolean testFieldSetS() {
		return (fieldSetS == 32767);
	}

	public boolean testFieldSetI() {
		return (fieldSetI == 2147483467);
	}

	public boolean testFieldSetJ() {
		return (fieldSetJ == 2147483467);
	}

	public boolean testFieldSetF() {
		return (Math.abs(fieldSetF - 1.23456789f) < EPSILON);
	}

	public boolean testFieldSetD() {
		return (Math.abs(fieldSetD - 1.23456789) < EPSILON);
	}
}
