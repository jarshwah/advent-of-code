import utils


def same_plot(grid: utils.Grid[str], node: utils.Point, neighbour: utils.Point) -> bool:
    return grid[node] == grid[neighbour]


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        """
        Traverse the grid, grouping each connected regions.

        For each region, calculate the area and multiply it by the perimeter.
        """
        grid = input.grid()
        regions: list[tuple[str, set[utils.Point]]] = []
        accounted: set[utils.Point] = set()
        for point in grid:
            if point in accounted:
                continue
            group = set(grid.collect_while(point, same_plot, diagonal=False))
            regions.append((grid[point], group))
            accounted |= group

        price = 0
        for _, reg in regions:
            area = len(reg)
            perimeter = sum(
                1 for nb in reg for _ in grid.get_neigbours_wrapping(nb) if _ not in reg
            )
            price += area * perimeter
        return price

    def part_two(self, input: utils.Input) -> str | int:
        """
        Traverse the grid, grouping each connected regions.

        For each region, calculate the area and multiply it by the number of sides.
        """
        grid = input.grid()
        regions: list[tuple[str, set[utils.Point]]] = []
        accounted: set[utils.Point] = set()
        for point in grid:
            if point in accounted:
                continue
            group = set(grid.collect_while(point, same_plot, diagonal=False))
            regions.append((grid[point], group))
            accounted |= group

        price = 0
        for _, reg in regions:
            area = len(reg)
            corners = len(utils.all_corners(reg))
            new_price = area * corners
            price += new_price
        return price


puzzle = Puzzle(
    year=2024,
    day=12,
    test_answers=("1930", "1206"),
    test_input="""RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""",
)

if __name__ == "__main__":
    puzzle.cli()
