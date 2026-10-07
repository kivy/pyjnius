package org.jnius;

public class SignatureTest {

    public static class IntOrLong {
        boolean was_long;
        public IntOrLong(int i) { was_long = false; }
        public IntOrLong(long l) { was_long = true; }
    }

    public static class ShortOrLong {
        boolean was_short;
        public ShortOrLong(short i) { was_short = true; }
        public ShortOrLong(long i) { was_short = false; }
    }
    
    public static class ShortOnly {
        public ShortOnly(short i) { }
        public ShortOnly(boolean o) { } // we need alternative constructor to force calculate_score
    }

}
