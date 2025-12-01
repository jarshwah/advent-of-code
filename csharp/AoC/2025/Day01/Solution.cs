namespace AdventOfCode.Y2025.Day01;

using System.Collections.Generic;
using System.Linq;


[ProblemName("Secret Entrance")]
class Solution : Solver
{

    static IEnumerable<(char direction, int clicks)> Parse(string input)
    {
        return input.Split("\n")
                   .Select(line => (direction: line[0], clicks: int.Parse(line[1..])));
    }

    public object PartOne(string input)
    {
        return Parse(input)
            .Aggregate(
                new { Position = 50, Zeros = 0 },
                (acc, next) =>
                {
                    var movement = next.direction == 'R' ? next.clicks : -next.clicks;
                    var newPosition = (acc.Position + movement) % 100;
                    return new { Position = newPosition, Zeros = acc.Zeros + (newPosition == 0 ? 1 : 0) };
                })
            .Zeros;
    }

    public object PartTwo(string input)
    {
        return Parse(input)
            .SelectMany(move => Enumerable.Range(0, move.clicks).Select(_ => move.direction == 'R' ? 1 : -1))
            .Aggregate(
                new { Position = 50, Zeros = 0 },
                (acc, step) =>
                {
                    var newPosition = (acc.Position + step) % 100;
                    return new { Position = newPosition, Zeros = acc.Zeros + (newPosition == 0 ? 1 : 0) };
                })
            .Zeros;
    }
}
