using System;

namespace AdventOfCode
{
    public static class Utilities
    {
        public static void PrintLine(object str)
        {
            Console.WriteLine(str);
        }

        public static void Print(object str)
        {
            Console.Write(str);
        }

        public static string Reverse(this string str)
        {
            char[] arr = str.ToCharArray();
            Array.Reverse(arr);
            return new string(arr);
        }

        public static int Manhattan(this (int x, int y) a, (int x, int y) b)
        {
            return Math.Abs(a.x - b.x) + Math.Abs(a.y - b.y);
        }

        public static int Manhattan(this (int x, int y, int z) a, (int x, int y, int z) b)
        {
            return Math.Abs(a.x - b.x) + Math.Abs(a.y - b.y) + Math.Abs(a.z - b.z);
        }

        public static long Manhattan(this (long x, long y) a, (long x, long y) b)
        {
            return Math.Abs(a.x - b.x) + Math.Abs(a.y - b.y);
        }

        public static long Manhattan(this (long x, long y, long z) a, (long x, long y, long z) b)
        {
            return Math.Abs(a.x - b.x) + Math.Abs(a.y - b.y) + Math.Abs(a.z - b.z);
        }

        public static double GCD(double a, double b)
        {
            if (a == 0 || b == 0) return Math.Max(a, b);
            return (a % b == 0) ? b : GCD(b, a % b);
        }

        public static double LCM(double a, double b) => a * b / GCD(a, b);

        public static long GCD(long a, long b)
        {
            if (a == 0 || b == 0) return Math.Max(a, b);
            return (a % b == 0) ? b : GCD(b, a % b);
        }

        public static long LCM(long a, long b) => a * b / GCD(a, b);

        public static (long q, long r) DivMod(long a, long b) => (a / b, a % b);

        public static int Mod(int x, int m)
        {
            int r = x % m;
            return r < 0 ? r + m : r;
        }

        public static long Mod(long x, long m)
        {
            long r = x % m;
            return r < 0 ? r + m : r;
        }


    }
}
