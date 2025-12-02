using System;
using System.Linq;

namespace AdventOfCode;

public static class EnumerableExtensions
{
    public static IEnumerable<int> Cumulative(this IEnumerable<int> sequence, int seed, Func<int, int, int> applier)
    {
        int acc = seed;
        foreach (var item in sequence)
        {
            acc = applier(acc, item);
            yield return acc;
        }
    }

}
