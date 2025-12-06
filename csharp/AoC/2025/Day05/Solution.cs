namespace AdventOfCode.Y2025.Day05;

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
using System.Text.RegularExpressions;
using System.Text;
using System.Numerics;
using static AdventOfCode.Utilities;

[ProblemName("Cafeteria")]
class Solution : Solver
{

    public object PartOne(string input)
    {
        var rangesAndIngredients = input.Split("\n\n", 2);
        var ranges = CompressRanges(ParseRanges(rangesAndIngredients[0]));
        var ingredients = ParseIngredients(rangesAndIngredients[1]);
        return ingredients
            .Where(ingredient =>
                ranges.Any(range => ingredient >= range.Item1 && ingredient <= range.Item2)
            )
            .Count();
    }

    public object PartTwo(string input)
    {
        return CompressRanges(
                ParseRanges(input.Split("\n\n", 2)[0])
            ).Sum(range => range.Item2 - range.Item1 + 1);
    }

    public static IEnumerable<(long, long)> ParseRanges(string rangeLines)
    {
        return rangeLines.Split("\n")
            .Select(rng => rng.Split("-", 2))
            .Select(pair => (long.Parse(pair[0]), long.Parse(pair[1])));
    }

    public static IEnumerable<long> ParseIngredients(string ingredientLines)
    {
        return ingredientLines.Split("\n").Select(ingredient => long.Parse(ingredient));
    }

    public static List<(long, long)> CompressRanges(IEnumerable<(long, long)> ranges)
    {
        List<(long, long)> compressed = [];
        var rangeList = ranges.OrderBy(pair => pair.Item1).ToList();
        var start = rangeList[0].Item1;
        var end = rangeList[0].Item2;

        foreach (var range in rangeList.Skip(1))
        {
            if (range.Item1 <= end)
            {
                end = long.Max(range.Item2, end);
                continue;
            }
            compressed.Add((start, end));
            start = range.Item1;
            end = range.Item2;
        }
        compressed.Add((start, end));
        return compressed;
    }


}
