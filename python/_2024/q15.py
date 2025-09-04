import utils

type Point = utils.Point


def score(grid: utils.Grid[str], box: str = "O") -> int:
    gps = 0
    for row, col in grid:
        if grid[row, col] == box:
            gps += 100 * row + col
    return gps


class Puzzle(utils.Puzzle):
    """
    A robot moves around the grid pushing boxes.

    Boxes can push other boxes, but only if there is a free space behind them.
    """

    def part_one(self, input: utils.Input) -> str | int:
        grid_map, instructions = input.group(sep="\n").strings
        moves = "".join(instructions)
        grid = utils.Grid(rows=grid_map)
        self.push_boxes(grid, moves)
        return score(grid, "O")

    def part_two(self, input: utils.Input) -> str | int:
        """
        Same, but double the width of all tiles.
        """
        grid_map, instructions = input.group(sep="\n").strings
        moves = "".join(instructions)
        expanded_map = []
        for row in grid_map:
            expanded_map.append(
                row.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
            )
        grid = utils.Grid(rows=expanded_map)
        self.push_boxes(grid, moves)
        return score(grid, "[")

    def push_boxes(self, grid: utils.Grid[str], moves: str) -> None:
        robot = grid.find("@")
        for move in moves:
            path: list[set[Point]] = [{robot}]
            while path:
                next_path = set()
                frontier = path[-1]
                for box in frontier:
                    new_box = utils.moves(box, move)
                    if new_box in frontier:
                        # neighbour while moving left or right
                        continue
                    if grid[new_box] == "#":
                        # If we hit a wall, then the entire move is invalid.
                        path.clear()
                        break
                    if grid[new_box] == ".":
                        # If we hit a free space, we can move the box there.
                        continue
                    # Otherwise, we've hit a box. Push the entire thing into the set.
                    if grid[new_box] == "[":
                        next_path.add(new_box)
                        neighbor = utils.moves(new_box, ">")
                        # But not if we're going left/right, it's already in there.
                        if neighbor not in frontier:
                            next_path.add(neighbor)
                    if grid[new_box] == "]":
                        next_path.add(new_box)
                        neighbor = utils.moves(new_box, "<")
                        if neighbor not in frontier:
                            next_path.add(neighbor)
                    if grid[new_box] == "O":
                        next_path.add(new_box)

                if not path:
                    break

                if next_path:
                    path.append(next_path)
                    # Keep pushin!
                    continue

                # We can push them all!
                # Prevent overwrites
                originals = {box: grid[box] for frontier in path for box in frontier}
                for frontier in reversed(path):
                    originals = {box: grid[box] for box in frontier}
                    for box in frontier:
                        if move in "^v":
                            # Hack: if we're going up or down, boxes won't push through each other,
                            # so we can clear the space behind them.
                            grid[box] = "."
                        grid[utils.moves(box, move)] = originals[box]

                if path:
                    # Update the robot's position. It's tile has already been moved.
                    grid[robot] = "."
                    robot = utils.moves(path[0].pop(), move)
                break


puzzle = Puzzle(
    year=2024,
    day=15,
    test_answers=("2028", "618"),
    test_input="""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<""",
    test_input_2="""#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^""",
)

if __name__ == "__main__":
    puzzle.cli()
