namespace AdventOfCode.Y2025.Day02;

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
using System.Text.RegularExpressions;
using System.Text;
using System.Numerics;
using static AdventOfCode.Utilities;

[ProblemName("Gift Shop")]
class Solution : Solver
{

    public object PartOne(string input)
    {
        // If a repeating prefix exists, sum the matching product ids together.
        // Must repeat exactly twice eg: 123123.
        return input.Split(",")
            .Select(range => range.Split("-"))
            .Select(pair => (long.Parse(pair[0]), long.Parse(pair[1])))
            .SelectMany(pair => Ranges.Range(pair.Item1, pair.Item2 + 1))
            .Sum(productId => IsRepeating(
                productId,
                minimumLength: (int)Math.Ceiling((double)productId.ToString().Length / 2))
                ? productId : 0
            );
    }

    public object PartTwo(string input)
    {
        // If a repeating prefix exists, sum the matching product ids together.
        // Must repeat at least twice eg: 123123123.
        return input.Split(",")
            .Select(range => range.Split("-"))
            .Select(pair => (long.Parse(pair[0]), long.Parse(pair[1])))
            .SelectMany(pair => Ranges.Range(pair.Item1, pair.Item2 + 1))
            .Sum(productId => IsRepeating(productId, minimumLength: 1) ? productId : 0);
    }



    static bool IsRepeating(long productId, int minimumLength)
    {
        var strpid = productId.ToString();
        var strlen = strpid.Length;
        // Generate all prefixes (up to half way) that match a minimum length
        // Then concat them together N times, and check if it matches the original string.
        return Ranges.Range(1, strlen / 2 + 1)
            .Where(len => len >= minimumLength)
            .Select(len => strpid.Substring(0, len))
            .Where(prefix => string.Join("", Enumerable.Repeat(prefix, strlen / prefix.Length)) == strpid)
            .Any();
    }
}
