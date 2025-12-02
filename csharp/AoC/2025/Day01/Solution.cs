namespace AdventOfCode.Y2025.Day01;

using System.Collections.Generic;
using System.Linq;
using AngleSharp.Css.Dom;

[ProblemName("Secret Entrance")]
class Solution : Solver
{

    static IEnumerable<(int direction, int clicks)> Parse(string input)
    {
        return input.Split("\n")
                   .Select(line => (direction: line[0] == 'R' ? 1 : -1, clicks: int.Parse(line[1..])));
    }

    public object PartOne(string input)
    {
        return Parse(input)
            .Select((move, direction) => move.clicks * move.direction)
            .Cumulative(50, (pos, step) => (pos + step) % 100)
            .Count(x => x == 0);
    }


    public object PartTwo(string input)
    {
        return Parse(input)
            .SelectMany(move => Enumerable.Range(0, move.clicks).Select(_ => move.direction))
            .Cumulative(50, (pos, step) => (pos + step) % 100)
            .Count(x => x == 0);
    }
}
