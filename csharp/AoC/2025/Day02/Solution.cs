namespace AdventOfCode.Y2025.Day02;

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
using System.Text.RegularExpressions;
using System.Text;
using System.Numerics;

[ProblemName("Gift Shop")]
class Solution : Solver
{

    public object PartOne(string input)
    {
        return input.Split(",")
            .Select(range => range.Split("-"))
            .Select(pair => (long.Parse(pair[0]), long.Parse(pair[1])))
            .SelectMany(pair => Ranges.Range(pair.Item1, pair.Item2 + 1))
            .Sum(productId => Repeating(productId, minimumLength: (int)Math.Ceiling((double)productId.ToString().Length / 2)));
    }

    public object PartTwo(string input)
    {
        return input.Split(",")
            .Select(range => range.Split("-"))
            .Select(pair => (long.Parse(pair[0]), long.Parse(pair[1])))
            .SelectMany(pair => Ranges.Range(pair.Item1, pair.Item2 + 1))
            .Sum(productId => Repeating(productId, minimumLength: 1));
    }



    static long Repeating(long productId, int minimumLength)
    {
        var strpid = productId.ToString();
        var strlen = strpid.Length;
        return Ranges.Range(1, strlen / 2 + 1)
            .Where(len => len >= minimumLength)
            .Select(len => strpid.Substring(0, len))
            .Where(prefix => string.Join("", Enumerable.Repeat(prefix, strlen / prefix.Length)) == strpid)
            .Any() ? productId : 0;
    }
}
