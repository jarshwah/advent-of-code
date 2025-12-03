namespace AdventOfCode.Y2025.Day03;

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
using System.Text.RegularExpressions;
using System.Text;
using System.Numerics;
using static AdventOfCode.Utilities;

[ProblemName("Lobby")]
class Solution : Solver
{

    public object PartOne(string input)
    {
        return Parse(input).Sum(nums => BestBatteries(nums, 2));
    }

    public object PartTwo(string input)
    {
        return Parse(input).Sum(nums => BestBatteries(nums, 12));
    }

    static IEnumerable<List<int>> Parse(string input)
    {
        return input.Split("\n")
                    .Select(line => line.ToCharArray())
                    .Select(chars => chars.Select(num => int.Parse(num.ToString())).ToList())
                    ;
    }

    static long BestBatteries(List<int> bank, int num)
    {
        var start = 0;
        var end = num - 1;
        var collect = new List<int>();
        while (num-- > 0)
        {
            start = bank.IndexOf(bank[start..^end].Max(), start);
            collect.Add(bank[start]);
            start++;
            end--;
        }
        return long.Parse(string.Join("", collect));
    }
}
