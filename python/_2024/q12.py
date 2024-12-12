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
            corners = get_corners(grid, reg)
            new_price = area * corners
            price += new_price
        return price


def get_corners(grid: utils.Grid[str], group: set[utils.Point]) -> int:
    """
    Get the number of corners in the group.

    The number of corners are equal to the number of sides.

    We need to compute internal and external corners differently, since internal
    corners can "belong" to too many nodes.
    """
    # get the points on the edge
    edges = set()
    for point in group:
        for neighbour in grid.get_neigbours_wrapping(point):
            if neighbour not in group:
                edges.add(point)
                break

    VERTICAL = [utils.UP, utils.DOWN]
    HORIZONTAL = [utils.LEFT, utils.RIGHT]

    # External Corners - match the number of neighbours in the vertical and horizontal directions.
    ext_corners = 0
    for edge in edges:
        V = len(
            [nb for nb in grid.get_neigbours_wrapping(edge, directions=VERTICAL) if nb in group]
        )
        H = len(
            [nb for nb in grid.get_neigbours_wrapping(edge, directions=HORIZONTAL) if nb in group]
        )
        # External corners
        match (V, H):
            case (0, 0):
                # No neighbours, fully fenced.
                ext_corners += 4
            case (0, 1) | (1, 0):
                #  x--  or X
                #          |
                ext_corners += 2
            case (1, 1):
                #  x--
                #  |
                ext_corners += 1
            case (2, 0) | (0, 2):
                #          |
                #  -x-  or x
                #          |
                ext_corners += 0
            case (2, 1) | (1, 2):
                #    |
                #  --x--
                #
                ext_corners += 0

            case _:
                raise ValueError(f"Invalid edge: {edge}, {V}, {H}")

    int_corners = 0
    # Internal Corners - find missing corners that have 3 neighbours.
    add = utils.point_add
    UL, UP, UR, R, DR, D, DL, L = utils.DIRECTIONS_8
    for p in group:
        if add(p, L) in group and add(p, UP) in group and add(p, UL) not in group:
            # X .
            # . .
            int_corners += 1
        if add(p, UP) in group and add(p, R) in group and add(p, UR) not in group:
            # . X
            # . .
            int_corners += 1
        if add(p, R) in group and add(p, D) in group and add(p, DR) not in group:
            # . .
            # . X
            int_corners += 1
        if add(p, D) in group and add(p, L) in group and add(p, DL) not in group:
            # . .
            # X .
            int_corners += 1

    return int_corners + ext_corners


if __name__ == "__main__":
    runner = Puzzle(
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
    runner.cli()
