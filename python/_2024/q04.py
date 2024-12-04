import utils


def xmas(grid: utils.Grid[str], curr: utils.Point, direction: utils.Point) -> bool:
    for letter in "XMAS":
        if grid.get(curr) != letter:
            return False
        curr = utils.point_add(curr, direction)
    return True


def mas(grid: utils.Grid[str], curr: utils.Point) -> bool:
    if grid[curr] != "A":
        return False
    return all(
        {grid.get(nb) for nb in grid.get_neighbours(curr, directions=pair)} == {"M", "S"}
        for pair in [(utils.UPLEFT, utils.DOWNRIGHT), (utils.UPRIGHT, utils.DOWNLEFT)]
    )


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        """
        Find XMAS in all 8 directions from each point in the grid.
        """
        grid = input.grid()
        return sum(
            xmas(grid, pos, direction) for pos in grid.points for direction in utils.DIRECTIONS_8
        )

    def part_two(self, input: utils.Input) -> str | int:
        """
        Find X-MAS where the M and S are in the diagonals of the A.

            M M       S M
             A         A
            S S       M S
        """
        grid = input.grid()
        return sum(mas(grid, pos) for pos in grid.points)


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=4,
        test_answers=("18", "9"),
        test_input="""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""",
    )
    runner.cli()
