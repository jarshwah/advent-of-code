using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics.CodeAnalysis;
using System.Drawing;

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

        public record Point(long Row, long Col)
        {
            public Point Add(Point point) => new(point.Row + Row, point.Col + Col);

            public Point Subtract(Point point) => new(point.Row - Row, point.Col - Col);

            public long Manhattan(Point point)
            {
                return Math.Abs(point.Row - Row) + Math.Abs(point.Col - Col);
            }
        }

        public static class Direction
        {
            public static readonly Point Center = new(0, 0);
            public static readonly Point Up = new(-1, 0);
            public static readonly Point Down = new(1, 0);
            public static readonly Point Left = new(0, -1);
            public static readonly Point Right = new(0, 1);
            public static readonly Point UpLeft = new(-1, -1);
            public static readonly Point UpRight = new(-1, 1);
            public static readonly Point DownLeft = new(1, -1);
            public static readonly Point DownRight = new(1, 1);

            public static readonly IList<Point> Directions4 = [Up, Right, Down, Left];
            public static readonly IList<Point> Directions8 = [Up, UpRight, Right, DownRight, Down, DownLeft, Left, UpLeft];

            public static Point TurnRight(Point direction)
            {
                return Directions4[(Directions4.IndexOf(direction) + 1) % 4];
            }

            public static Point TurnLeft(Point direction)
            {
                return Directions4[Mod(Directions4.IndexOf(direction) + 1, 4)];
            }
        }

        public static IEnumerable<IEnumerable<T>> Transpose<T>(IEnumerable<IEnumerable<T>> rows)
        {
            var length = rows.First().Count();
            for (int i = 0; i < length; i++)
            {
                yield return rows.Select(row => row.Skip(i).First());
            }
        }
    }

    public class Grid<T> : IReadOnlyDictionary<Utilities.Point, T>
    {
        public readonly IDictionary<Utilities.Point, T> points;
        public readonly int NumRows;
        public readonly int NumCols;

        public IEnumerable<IEnumerable<T>> Rows => points.OrderBy(p => p.Key.Row).ThenBy(p => p.Key.Col).Select(p => p.Value).Chunk(NumCols);
        public IEnumerable<IEnumerable<T>> Cols => points.OrderBy(p => p.Key.Col).ThenBy(p => p.Key.Row).Select(p => p.Value).Chunk(NumCols);

        public Grid(IEnumerable<IEnumerable<T>> points)
        {
            this.points = new Dictionary<Utilities.Point, T>();
            int rc = 0;
            foreach (var row in points)
            {
                int cc = 0;
                foreach (var col in row)
                {
                    this.points.Add(new Utilities.Point(rc, cc), col);
                    cc++;
                }
                rc++;
            }
            NumRows = points.Count();
            NumCols = points.First().Count();
        }

        public IEnumerable<Utilities.Point> Keys => points.Keys;

        public IEnumerable<T> Values => points.Values;

        public int Count => NumRows * NumCols;

        public T this[Utilities.Point key] => points[key];

        public bool ContainsKey(Utilities.Point key)
        {
            return points.ContainsKey(key);
        }

        public bool TryGetValue(Utilities.Point key, [MaybeNullWhen(false)] out T value)
        {
            return points.TryGetValue(key, out value);
        }

        public IEnumerator<KeyValuePair<Utilities.Point, T>> GetEnumerator()
        {
            return points.GetEnumerator();
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return GetEnumerator();
        }
    }
}
