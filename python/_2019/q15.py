import time
from collections import defaultdict, deque
from enum import IntEnum, StrEnum
from typing import assert_never

import intcode

import utils

type Point = utils.Point
type Droid = Point
type Input = int
type Direction = Point
type State = tuple[Droid, intcode.IntCode, Command]


class Tile(StrEnum):
    EMPTY = " "
    WALL = "#"
    OXYGEN_SYSTEM = "O"
    UNKNOWN = "?"
    DROID = "x"


class Command(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


class Status(IntEnum):
    WALL = 0
    MOVED = 1
    FOUND = 2


def new_pos(droid: Droid, command: Command) -> Point:
    match command:
        case Command.NORTH:
            return utils.moves(droid, "^")
        case Command.SOUTH:
            return utils.moves(droid, "v")
        case Command.WEST:
            return utils.moves(droid, "<")
        case Command.EAST:
            return utils.moves(droid, ">")
        case _:
            assert_never()


class Puzzle(utils.Puzzle):
    def both_parts(self, input: utils.Input) -> tuple[str | int, str | int]:
        init = intcode.IntCode(input.split(",").numbers)
        grid = utils.Grid.from_string("")
        start = (0, 0)
        grid[start] = Tile.DROID
        states: deque[State] = deque([(start, init.fork(), command) for command in Command])
        animate = True
        with grid.animate(on=animate) as animator:
            while states:
                droid, program, command = states.popleft()
                move_to = new_pos(droid, command)
                if move_to in grid:
                    continue

                if animate:
                    animator.update(grid, header="MAPPING")

                program.input.write(command)
                response = next(program.output)
                match Status(response):
                    case Status.WALL:
                        grid[move_to] = Tile.WALL
                    case Status.MOVED:
                        grid[move_to] = Tile.EMPTY
                        states.extend([(move_to, program.fork(), command) for command in Command])
                    case Status.FOUND:
                        grid[move_to] = Tile.OXYGEN_SYSTEM
                        states.extend([(move_to, program.fork(), command) for command in Command])

            oxygen_position = grid.find(Tile.OXYGEN_SYSTEM)
            path_to_oxygen = utils.dijkstra_shortest_path(
                grid, start, oxygen_position, unmovable=Tile.WALL
            )
            path_to_droid = utils.dijkstra_best_score(grid, oxygen_position, droid, unmovable="#")
            steps_to_oxygen = len(path_to_oxygen) - 1
            time_to_fill = max(steps for steps in path_to_droid.values())

            if animate:
                for wall_point in grid.find_all(Tile.WALL):
                    grid[wall_point] = utils.Color.BLUE_VIOLET.colorize(Tile.WALL)
                for step in path_to_oxygen:
                    grid[step] = utils.Color.YELLOW_BRIGHT.colorize(Tile.DROID)
                    animator.update(grid, header="FINDING OXYGEN")
                    time.sleep(15 / steps_to_oxygen)

                oxygen_fill_steps = defaultdict(list)
                for point, steps in path_to_droid.items():
                    oxygen_fill_steps[steps].append(point)

                for t in sorted(oxygen_fill_steps.keys()):
                    for pt in oxygen_fill_steps[t]:
                        grid[pt] = utils.Color.GREEN.colorize(Tile.OXYGEN_SYSTEM)
                    animator.update(grid, header="OXYGENATING")
                    time.sleep(15 / time_to_fill)

        return steps_to_oxygen, time_to_fill


if __name__ == "__main__":
    runner = Puzzle(
        year=2019,
        day=15,
        both=True,
        no_tests=True,
    )
    runner.cli()
