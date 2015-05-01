package org.jnius;

public class MultipleDimensions {
	public static boolean methodParamsMatrixI(int[][] x) {
		if (x.length != 3 || x[0].length != 3)
			return false;
		return (x[0][0] == 1 && x[0][1] == 2 && x[1][2] == 6);
	}
	public static int[][] methodReturnMatrixI() {
        int[][] matrix = {{1,2,3},
                          {4,5,6},
                          {7,8,9}};
        return matrix;
	}

}
