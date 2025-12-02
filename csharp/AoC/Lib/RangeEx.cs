using System.Linq.Expressions;

namespace AdventOfCode;

static class Ranges
{
    public static IEnumerable<long> Range(long start, long end)
    {
        while (start < end)
        {
            yield return start;
            start++;
        }
    }

    public static IEnumerable<int> Range(int start, int end)
    {
        while (start < end)
        {
            yield return start;
            start++;
        }
    }
}
