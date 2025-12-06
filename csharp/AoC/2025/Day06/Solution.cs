namespace AdventOfCode.Y2025.Day06;

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
using System.Text.RegularExpressions;
using System.Text;
using System.Numerics;
using static AdventOfCode.Utilities;
using AngleSharp.Css.Dom;
using AngleSharp.Text;
using System.Runtime.Serialization.Formatters;

[ProblemName("Trash Compactor")]
class Solution : Solver
{

    public object PartOne(string input)
    {
        var tokenized = input.Split("\n").Select(line => line.Split(" ", StringSplitOptions.RemoveEmptyEntries));
        return Transpose(
            tokenized
                .TakeWhile(tokens => int.TryParse(tokens.First(), out int intParse))
                .Select(numList => numList.Select(int.Parse))
        ).Zip(tokenized.Last())
        .Select(zipped => zipped.Second == "*" ?
            zipped.First.Aggregate(1L, (left, right) => left * right)
            : zipped.First.Sum()
        ).Sum();
    }

    public object PartTwo(string input)
    {
        var tokenized = Transpose(input.Split("\n"));
        var nums = tokenized
            .Where(line => !string.IsNullOrWhiteSpace(string.Concat(line)))
            .Select(line =>
                int.Parse(new string([.. line.Where(c => int.TryParse(c.ToString(), out int intParse))]))
        ).GetEnumerator();
        var operators = tokenized.SelectMany(line => line.Where(ch => "+*".Contains(ch))).GetEnumerator();
        var equationBreaks = tokenized.Select(line => line.All(ch => ch == ' '));
        return Calculate(nums, operators, equationBreaks).Sum();
    }

    private static IEnumerable<long> Calculate(
        IEnumerator<int> nums,
        IEnumerator<char> operators,
        IEnumerable<bool> equationBreaks
    )
    {
        nums.MoveNext();
        operators.MoveNext();
        List<int> currentNums = [];
        foreach (var isBreak in equationBreaks)
        {
            if (isBreak)
            {
                yield return Aggregate(operators, currentNums);
                operators.MoveNext();
                currentNums.Clear();
                continue;
            }
            currentNums.Add(nums.Current);
            nums.MoveNext();
        }
        yield return Aggregate(operators, currentNums);

        static long Aggregate(IEnumerator<char> operators, List<int> currentNums)
        {
            return operators.Current == '*'
                ? currentNums.Aggregate(1L, (left, right) => left * right)
                : currentNums.Sum();
        }
    }
}
