// Decompiled by Jad v1.5.8e. Copyright 2001 Pavel Kouznetsov.
// Jad home page: http://www.geocities.com/kpdus/jad.html
// Decompiler options: packimports(3) 
// Source File Name:   problem.java

import java.io.PrintStream;
import java.util.Arrays;
import java.util.Base64;

public class problem
{

    public problem()
    {
    }

    public static String get_flag()
    {
        String s = "Hint: Don't worry about the schematics";
        String s1 = "eux_Z]\\ayiqlog`s^hvnmwr[cpftbkjd";
        String s2 = "Zf91XhR7fa=ZVH2H=QlbvdHJx5omN2xc";
        byte abyte0[] = s1.getBytes();
        byte abyte1[] = s2.getBytes();
        byte abyte2[] = new byte[abyte1.length];
        for(int i = 0; i < abyte1.length; i++)
            abyte2[i] = abyte1[abyte0[i] - 90];

        System.out.println(Arrays.toString(Base64.getDecoder().decode(abyte2)));
        return new String(Base64.getDecoder().decode(abyte2));
    }

    public static void main(String args[])
    {
        System.out.println("FLAG=" + get_flag());
    }
}
