package org.jnius;

public class VariablePassing {

  public VariablePassing() {

  }

  public VariablePassing(int[] numbers) {
    squareNumbers(numbers);
  }

  public VariablePassing(int[] numbers1, int[] numbers2, int[] numbers3, int[] numbers4) {
    squareNumbers(numbers1);
    squareNumbers(numbers2);
    squareNumbers(numbers3);
    squareNumbers(numbers4);
  }

  private static void squareNumbers(int[] numbers) {
    for (int i = 0; i < numbers.length; i++) {
      numbers[i] = i * i;
    }
  }

  public static void singleParamStatic(int[] numbers) {
    squareNumbers(numbers);
  }

  public static void multipleParamsStatic(int[] numbers1, int[] numbers2, int[] numbers3, int[] numbers4) {
    squareNumbers(numbers1);
    squareNumbers(numbers2);
    squareNumbers(numbers3);
    squareNumbers(numbers4);
  }

  public void singleParam(int[] numbers) {
    squareNumbers(numbers);
  }

  public void multipleParams(int[] numbers1, int[] numbers2, int[] numbers3, int[] numbers4) {
    squareNumbers(numbers1);
    squareNumbers(numbers2);
    squareNumbers(numbers3);
    squareNumbers(numbers4);
  }
}
