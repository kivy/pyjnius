// javac arraylist.java
// java arraylist

import java.lang.String;
import java.util.List;
import java.util.Arrays;
import java.util.ArrayList;


public class arraylist {
    public static void main(String[] args) {
        // Object based empty ArrayList
        ArrayList<Object> jlist = new ArrayList<Object>();
        System.out.println(jlist);
        System.out.println(jlist.size());

        // String array
        String[] str_array = {"a", "b", "c"};
        System.out.println(str_array.toString());
        System.out.println(str_array.length);

        // add the array of strings to the list
        jlist.add(str_array);
        System.out.println(jlist.toString());
        System.out.println(jlist.size());

        // create a new ArrayList from String array
        ArrayList<Object> str_list = new ArrayList<Object>(
            Arrays.asList(str_array.toString())
        );
        jlist.add(str_list);
        System.out.println(jlist.toString());
        System.out.println(jlist.size());

        // add an empty Object to ArrayList
        jlist.add(new Object());
        System.out.println(jlist.toString());
        System.out.println(jlist.size());

        // new ArrayList to wrap everything up
        ArrayList plain_list = new ArrayList();
        plain_list.add(str_array);
        plain_list.add(str_list);
        plain_list.add(jlist);
        System.out.println(plain_list.toString());
        System.out.println(plain_list.size());
    }
}
