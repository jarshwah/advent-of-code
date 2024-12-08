from __future__ import annotations

import dataclasses
import itertools
from collections import deque
from collections.abc import Callable, Iterable, Iterator, Sequence
from copy import deepcopy
from functools import cached_property
from typing import Generator, Self

import aocd
import networkx as nx
import parse
import rich_click as click

type Point = tuple[int, int]
type Point3d = tuple[int, int, int]
type Point4d = tuple[int, int, int, int]
type PointNd = tuple[int, ...]
SENTINEL = object()


@dataclasses.dataclass
class Input:
    data: str

    @property
    def string(self) -> str:
        """Return the input data as a string"""
        return self.data

    @property
    def integer(self) -> int:
        """Return the input data as an integer"""
        return int(self.data)

    @property
    def number(self) -> int:
        """Return the input data as an integer"""
        return self.integer

    @property
    def float(self) -> float:
        """Return the input data as a float"""
        return float(self.data)

    def parse(self, parser: str) -> parse.Match | None:
        """Parse the input data using the provided parser returning a Match or None"""
        return parse.parse(parser, self.string)

    def lines(self) -> InputList:
        """
        Split the input data into lines separated by newlines.
        """
        return self.split("\n")

    def columns(self) -> InputGroup:
        """
        Split the input data into lines then rotate into columns.
        """
        return InputGroup(data=[InputList(data=col) for col in zip(*self.lines().split().data)])

    def split(self, sep: str | None = None) -> InputList:
        """
        Split the input data into lines separated by the provided separator.
        """
        return InputList(data=[Input(data=token) for token in self.data.split(sep)])

    def group(self, group: str | None = "\n\n", sep: str | None = None) -> InputGroup:
        """
        Group the input data into multiple lists of lists separated by the provided group separator.

        eg.

            1234
            5678

            abcde
            fghij

        would be grouped into (with \n\n as the default group separator):
            [[1234, 5678], [abcde, fghij]]


        """
        return self.split(group).split(sep)

    def grid(self) -> Grid[str]:
        """
        Create a Grid from lines of input data.
        """
        return Grid.from_string(self.data)

    def grid_int(self) -> Grid[int]:
        """
        Create a Grid of ints from lines of input data.
        """
        return Grid.from_number_string(self.data)


@dataclasses.dataclass
class InputList:
    """
    A list of strings.

    For example:

    ["1", "2", "3"]

    """

    data: Sequence[Input]

    @property
    def strings(self) -> Sequence[str]:
        """
        Return a list of strings, one for each line.
        """
        return [inp.string for inp in self.data]

    @property
    def integers(self) -> Sequence[int]:
        """
        Return a list of integers, one for each line.
        """
        return [inp.integer for inp in self.data]

    @property
    def numbers(self) -> Sequence[int]:
        """
        Return a list of integers, one for each line.
        """
        return self.integers

    @property
    def floats(self) -> Sequence[float]:
        """
        Return a list of floats, one for each line.
        """
        return [inp.float for inp in self.data]

    def parse(self, *parsers: str) -> Sequence[parse.Match]:
        """
        Return a list of parsed results, the first parser than matches each lines is used.
        """
        results: list[parse.Match] = []
        for s in self.strings:
            for p in parsers:
                if result := parse.parse(p, s):
                    results.append(result)
                    break
            else:
                raise ValueError(f"{s} was not parsed")
        return results

    def split(self, sep: str | None = None) -> InputGroup:
        """
        Return a group by splitting each line by the provided separator.
        """
        return InputGroup(data=[inp.split(sep) for inp in self.data])

    def __iter__(self) -> Iterable[Input]:
        return self.data.__iter__()


@dataclasses.dataclass
class InputGroup:
    """
    A list of lists.

    For example:

    [
        ["1", "2", "3"],
        ["4", "5", "6"],
    ]
    """

    data: Sequence[InputList]

    @property
    def strings(self) -> Sequence[Sequence[str]]:
        """
        Return a list of lists of strings.
        """
        return [inp.strings for inp in self.data]

    @property
    def integers(self) -> Sequence[Sequence[int]]:
        """
        Return a list of lists of integers.
        """
        return [inp.integers for inp in self.data]

    @property
    def numbers(self) -> Sequence[Sequence[int]]:
        """
        Alias for the integers property.
        """
        return self.integers

    @property
    def floats(self) -> Sequence[Sequence[float]]:
        """
        Return a list of lists of floats.
        """
        return [inp.floats for inp in self.data]

    def parse(self, *parsers: str) -> Sequence[Sequence[parse.Match]]:
        """
        Parse the input data using the provided parsers for each line within the group.
        """
        return [inp.parse(*parsers) for inp in self.data]

    def grid(self) -> Grid[str]:
        """
        Convert the input data to a grid of strings.
        """
        return Grid(rows=(s for string in self.strings for s in string))

    def grid_int(self) -> Grid[int]:
        """
        Convert the input data to a grid of integers.
        """
        return Grid(rows=((int(item) for item in row) for group in self.strings for row in group))

    def __iter__(self) -> Iterable[InputList]:
        return self.data.__iter__()


def int_numbers(input_data: str, sep: str | None = None) -> Sequence[int]:
    """Transform a line of numbers into a list of integers"""
    if sep is None:
        return [int(num) for num in input_data.splitlines() if num.strip()]
    return [int(num) for num in input_data.split(sep) if num.strip()]


def first[T](i: Iterable[T]) -> T:
    """Return the first item of the iterator or exception if empty"""
    return next(iter(i))


def only[T](i: Iterable[T]) -> T:
    """Return the only item of the iterator or exception if not exactly one item"""
    consumed = list(i)
    if len(consumed) != 1:
        raise ValueError(f"i had {len(consumed)} values")
    return consumed[0]


def sort_by_length[T](iterables: Iterable[Sequence[T]]) -> Iterable[Sequence[T]]:
    """
    Sort the iterable by length of the sequences.

    eg: sort_by_length([[1, 2], [1, 2, 3], [1]]) == [[1], [1, 2], [1, 2, 3]]
    """
    return sorted(iterables, key=len)


def line_algorithm(start: Point, end: Point) -> Iterable[Point]:
    """
    Finds all points between `start` and `end` points.

    A simple implementation of Bresenham's line drawing algorithm.
    """
    # attribution: https://github.com/encukou/bresenham
    x0, y0 = start
    x1, y1 = end

    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1
    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2 * dy - dx
    y = 0

    for x in range(int(dx) + 1):
        yield x0 + x * xx + y * yx, y0 + x * xy + y * yy
        if D >= 0:
            y += 1
            D -= 2 * dx
        D += 2 * dy


def partition[T](seq: Sequence[T], idx: int) -> tuple[Sequence[T], Sequence[T]]:
    """Split a sequence at the provided index"""
    return seq[:idx], seq[idx:]


def partition_middle[T](seq: Sequence[T]) -> tuple[Sequence[T], Sequence[T]]:
    """
    Split a sequence in half.

    If the list has an odd number of items, the first list will have one fewer item.
    """
    midpoint = len(seq) // 2
    return seq[:midpoint], seq[midpoint:]


def chunked[T](it: Iterable[T], n: int, fillvalue: T | None = None) -> Iterable[Iterable[T]]:
    """
    Split an iterable into chunks of size n, with the last chunk padded with fillvalue if necessary.

    Use itertools.batched for a version that doesn't pad the last chunk.
    """
    return itertools.zip_longest(*[iter(it)] * n, fillvalue=fillvalue)


def transpose[T](rows: Sequence[Sequence[T]]) -> Sequence[Sequence[T]]:
    """
    Transpose a list of lists so rows become columns and columns become rows.

    >>> transpose([[1, 2, 3], [4, 5, 6]])
        [[1, 4], [2, 5], [3, 6]]

    123  14
    456  25
         36
    """
    return list(map(list, zip(*rows)))


def rotate[T](rows: Sequence[Sequence[T]], rotations: int = 1) -> Sequence[Sequence[T]]:
    """
    Rotate a list of lists 90 degrees clockwise.

    >>> rotate([[1, 2, 3], [4, 5, 6]], 1)
        [[4, 1], [5, 2], [6, 3]]

    123  41  654  36
    456  52  321  25
         63       14
    """
    for _ in range(rotations % 4):
        rows = list(map(list, zip(*reversed(rows))))
    return rows


def triangle_number(n: int) -> int:
    """
    Compute the triange number

    The triangular number of 7 is 28

    1 + 2 + 3 + 4 + 5 + 6 + 7
    """
    return n * (n + 1) // 2


def shoelace(points: Sequence[Point]) -> int:
    """
    Find the area within a polygon, excluding the boundary
    """
    return area_inside_boundary(points)


def picks_theorem(num_points: int, inside_area: int) -> int:
    """
    Find the area of a polygon including the boundary
    """
    return inside_area + num_points // 2 + 1


def area_inside_boundary(points: Sequence[Point]) -> int:
    """
    Get the area of a polygon inside a boundary.

    AKA the shoelace theorem.
    """
    return (
        abs(
            sum(
                x1 * y2 - x2 * y1
                for (x1, y1), (x2, y2) in itertools.pairwise(list(points) + [points[0]])
            )
        )
        // 2
    )


def area_including_boundary(points: Sequence[Point]) -> int:
    """
    Get the area of a polygon including the boundary.

    Combines the shoelace and picks theorems.
    """
    return picks_theorem(len(points), shoelace(points))


def shoelace_iter(point: Point) -> Generator[int, Point, int]:
    """
    Compute the shoelace area iteratively.

    Usage:
        >>> area_gen = shoelace_iter(first_point)
        >>> next(area_gen)  # initialize
        >>> for point in points:
        ...    area_gen.send(point)
        >>> area = next(area_gen)
    """
    current: Point | None
    area = 0
    first = point
    prev = point
    while True:
        current = yield (area)
        if current is None:
            break  # type: ignore [unreachable]
        area += prev[0] * current[1] - prev[1] * current[0]
        prev = current
    area += prev[0] * first[1] - prev[1] * first[0]  # type: ignore [unreachable]
    yield abs(area) // 2


def manhattan(p1: PointNd, p2: PointNd) -> int:
    """
    Find the manhattan distance between two points.

    Uses straight line distance between two points in an N-dimensional space.

    >>> manhattan( (0,0), (10,10) )
    20
    """
    return sum(abs(a - b) for a, b in zip(p1, p2, strict=True))


def point_subtract[T: PointNd](p1: T, p2: T) -> T:
    """
    Subtract p2 from p1.

    >>> point_subtract( (10, 10), (2, 2) )
    (8, 8)
    """
    # We know the lengths will be the same, so ignore the type check on return value
    return tuple(a - b for a, b in zip(p1, p2, strict=True))  # type: ignore [return-value]


def point_add[T: PointNd](p1: T, p2: T, steps: int = 1) -> T:
    """
    Add p2 to p1.

    >>> point_add( (10, 10), (2, 2) )
    (12, 12)
    """
    # We know the lengths will be the same, so ignore the type check on return value
    return tuple(a + (steps * b) for a, b in zip(p1, p2, strict=True))  # type: ignore [return-value]


def sum_points(*points: Point) -> Point:
    """
    Sum a list of points.

    >>> sum_points( (10, 10), (2, 2), (3, 3) )
    (15, 15)
    """
    return sum(p[0] for p in points), sum(p[1] for p in points)


# Represented as ROW, COLUMN (or y,x)
CENTER = (0, 0)
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
UPLEFT = sum_points(UP, LEFT)
UPRIGHT = sum_points(UP, RIGHT)
DOWNLEFT = sum_points(DOWN, LEFT)
DOWNRIGHT = sum_points(DOWN, RIGHT)
DIRECTIONS_4: Sequence[Point] = [UP, RIGHT, DOWN, LEFT]
DIRECTIONS_8: Sequence[Point] = [
    UPLEFT,
    UP,
    UPRIGHT,
    RIGHT,
    DOWNRIGHT,
    DOWN,
    DOWNLEFT,
    LEFT,
]
DIRECTIONS_9: Sequence[Point] = [
    UPLEFT,
    UP,
    UPRIGHT,
    LEFT,
    CENTER,
    RIGHT,
    DOWNLEFT,
    DOWN,
    DOWNRIGHT,
]


def turn_right(direction: Point) -> Point:
    """
    Turn right for the given 4-directional point.

    >>> turn_right( DOWN ) == LEFT
    True
    """
    return DIRECTIONS_4[(DIRECTIONS_4.index(direction) + 1) % len(DIRECTIONS_4)]


def turn_left(direction: Point) -> Point:
    """
    Turn left for the given 4-directional point.

    >>> turn_left( DOWN ) == RIGHT
    True
    """
    return DIRECTIONS_4[(DIRECTIONS_4.index(direction) - 1) % len(DIRECTIONS_4)]


def neighbours(point: Point, directions: Sequence[Point]) -> Sequence[Point]:
    """
    Get the neighbours of a point in the given directions.

    >>> neighbours( (3, 3), DIRECTIONS_4)
    [(2, 3), (3, 4), (4, 3), (3, 2)]
    """
    return [(point[0] + d[0], point[1] + d[1]) for d in directions]


@dataclasses.dataclass
class Grid[T]:
    """
    Models a grid of (row, column) points with a value at each point.
    """

    points: dict[Point, T]

    def __init__(self, rows: Iterable[Iterable[T]], pad_with: T | None = None):
        self.points = {}
        self.pad_with = pad_with
        for r, row in enumerate(rows):
            for c, item in enumerate(row):
                self.points[(r, c)] = item

    @classmethod
    def from_number_string(
        cls, data: str, separator: str | None = None, pad_with: int | None = None
    ) -> Grid[int]:
        """
        Build a grid from a string of numbers, each row separated by a newline.
        """
        if separator:
            return Grid(
                rows=((int(n) for n in row.split(separator)) for row in data.splitlines()),
                pad_with=pad_with,
            )
        return Grid(rows=((int(n) for n in row) for row in data.splitlines()), pad_with=pad_with)

    @classmethod
    def from_string(
        cls, data: str, separator: str | None = None, pad_with: str | None = None
    ) -> Grid[str]:
        """
        Build a grid from a string, each row separated by a newline.
        """
        if separator:
            return Grid(
                rows=((n for n in row.split(separator)) for row in data.splitlines()),
                pad_with=pad_with,
            )
        return Grid(rows=((n for n in row) for row in data.splitlines()), pad_with=pad_with)

    def get(self, key: Point, default: T | None = None) -> T | None:
        return self.points.get(key, default)

    def __len__(self) -> int:
        """Number of points"""
        return self.points.__len__()

    def __iter__(self) -> Iterator[Point]:
        """Iterate over the points"""
        return self.points.__iter__()

    def __contains__(self, key: Point) -> bool:
        """Check if a point is in the grid"""
        return key in self.points

    def __getitem__(self, index: Point) -> T:
        """Get the value at a point if it exists or exception"""
        return self.points[index]

    def __setitem__(self, index: Point, value: T) -> None:
        self.points[index] = value

    def rows(self) -> Iterable[Sequence[T]]:
        """Iterate over the rows of the grid"""
        for r in range(self.height):
            yield [self[r, c] for c in range(self.width)]

    def cols(self) -> Iterable[Sequence[T]]:
        """Iterate over the columns of the grid"""
        for c in range(self.width):
            yield [self[r, c] for r in range(self.height)]

    @cached_property
    def width(self) -> int:
        """
        How wide the grid is.

        Assumes the grid is complete.
        """
        return max(self.points)[1] + 1

    @cached_property
    def height(self) -> int:
        """
        How tall the grid is.

        Assumes the grid is complete.
        """
        return max(self.points)[0] + 1

    @property
    def _directions(self) -> Sequence[Point]:
        return DIRECTIONS_4

    @property
    def _directions_diag(self) -> Sequence[Point]:
        return DIRECTIONS_8

    def get_neighbours(
        self, point: Point, diag: bool = False, directions: Sequence[Point] | None = None
    ) -> Iterable[Point]:
        """
        Get the neighbours of a point.

        If directions is provided, only return the neighbours in those directions.
        If diag is True, return diagonal neighbours as well as 4-directional neighbours.
        """
        if directions is None:
            directions = self._directions_diag if diag else self._directions
        for d in directions:
            p = sum_points(point, d)
            if p in self:
                yield p
            elif self.pad_with is not None:
                self[p] = self.pad_with
                yield p

    # alias for get_neighbours
    neighbours = get_neighbours

    def get_neigbours_wrapping(
        self, point: Point, diag: bool = False, directions: Sequence[Point] | None = None
    ) -> Iterable[Point]:
        """
        Get the neighbours of a point, wrapping around the grid if necessary.
        """
        height = self.height
        width = self.width
        if directions is None:
            directions = self._directions_diag if diag else self._directions
        for d in directions:
            p = sum_points(point, d)
            wrapped_p = (p[0] % height, p[1] % width)
            if wrapped_p in self:
                yield wrapped_p

    def find(self, value: T) -> Point:
        """
        Find the first point with the given value.
        """
        for point, v in self.points.items():
            if v == value:
                return point
        raise ValueError(f"{value} not found in grid")

    def search(
        self,
        comparison_func: Callable[[tuple[Point, T], Sequence[tuple[Point, T]]], bool],
        diagonal: bool = False,
    ) -> Iterable[tuple[Point, T]]:
        """
        For each point in the grid, check if it meets the comparison function with its neighbours.

        Yields (point, matching_neighbour) pairs.
        """
        for point in self.points.keys():
            neighbours = [(n, self.points[n]) for n in self.get_neighbours(point, diag=diagonal)]
            if comparison_func((point, self.points[point]), neighbours):
                yield point, self.points[point]

    def collect_recursive(
        self,
        start: Point,
        comparison_func: Callable[[tuple[Point, T], list[tuple[Point, T]]], bool],
        diagonal: bool = False,
    ) -> Iterable[tuple[Point, T]]:
        """
        Recursively collect all points that meet the comparison function from a starting point.
        """
        queue = deque([start])
        seen = set()
        found = set()
        while queue:
            p = queue.popleft()
            if p in seen:
                continue
            seen.add(p)
            neighbours = [(n, self.points[n]) for n in self.get_neighbours(p, diag=diagonal)]
            if comparison_func((p, self.points[p]), neighbours):
                found.add(p)
                queue.extend([n[0] for n in neighbours])
        return [(f, self.points[f]) for f in found]

    def to_graph(
        self,
        diagonal: bool = False,
        weighted: bool = True,
        directed: bool = True,
        is_connected_func: Callable[[Grid[T], Point, Point], bool] | None = None,
    ) -> nx.Graph[Point]:
        """
        Build a graph from the grid.

        Edges are created between neighbouring points that match the is_connected_func.
        """
        graph: nx.Graph[Point] = nx.DiGraph() if directed else nx.Graph()
        for point in self.__iter__():
            neighbours = self.get_neighbours(point, diag=diagonal)
            for nb in neighbours:
                if is_connected_func is None or is_connected_func(self, point, nb):
                    if weighted:
                        graph.add_edge(point, nb, weight=self[nb])
                    else:
                        graph.add_edge(point, nb)
        return graph

    def replicate(self, right: int, down: int) -> Grid[T]:
        """
        Grow the grid by replicating it right and down factors.

        0 and 1 are the same grid.

        123     123123
        456     456456
                123123
                456456
        """
        assert (
            right > 1 or down > 1
        ), "Replication must be greater than 1 in at least one direction"
        grid: Grid[T] = Grid([])
        length_r = self.width
        length_c = self.height
        grid = deepcopy(self)
        for ri in range(length_r):
            for ci in range(length_c):
                for newri in range(down):
                    for newci in range(right):
                        grid[length_r * newri + ri, length_c * newci + ci] = self[ri, ci]
        return grid

    def rotate(self, rotations: int = 1) -> Grid[T]:
        """
        Rotate the grid 90 degrees clockwise.
        """
        return Grid(rows=rotate(list(self.rows()), rotations=rotations))

    def transpose(self) -> Grid[T]:
        """
        Transpose the grid, so that rows become columns and columns become rows.
        """
        return Grid(rows=transpose(list(self.rows())))

    def print(self, missing: T | str = "?") -> None:
        """
        Print the grid to the console.
        """
        for row in self.strings(missing):
            print("".join(row))
        print()

    def strings(self, missing: T | str = "?") -> Sequence[str]:
        """
        Return the grid as a Sequence of strings.
        """
        rmin = min(self.points)[0]
        rmax = max(self.points)[0]
        cmin = min(node[1] for node in self.points)
        cmax = max(node[1] for node in self.points)

        return [
            "".join(str(self.points.get((r, c), missing)) for c in range(cmin, cmax + 1))
            for r in range(rmin, rmax + 1)
        ]

    def hash_key(self) -> str:
        """
        Make a hash key out of the content of the grid, so that it's hashable.
        """
        return "".join(self.strings())


def rotations_90(point: Point3d) -> list[Point3d]:
    """Produces all 24 90 degree rotations for a 3d Point"""
    x, y, z = point
    return [
        (x, y, z),
        (x, z, -y),
        (x, -y, -z),
        (x, -z, y),
        (y, x, -z),
        (y, z, x),
        (y, -x, z),
        (y, -z, -x),
        (z, x, y),
        (z, y, -x),
        (z, -x, -y),
        (z, -y, x),
        (-x, y, -z),
        (-x, z, y),
        (-x, -y, z),
        (-x, -z, -y),
        (-y, x, z),
        (-y, z, -x),
        (-y, -x, -z),
        (-y, -z, x),
        (-z, x, -y),
        (-z, y, x),
        (-z, -x, y),
        (-z, -y, -x),
    ]


@dataclasses.dataclass
class Puzzle:
    year: int
    day: int
    test_input: str = ""
    test_input_2: str = ""
    test_answers: tuple[str, str] = ("", "")

    def part_one(self, input: Input) -> str | int:
        return ""

    def part_two(self, input: Input) -> str | int:
        return ""

    def part_one_alt(self, input: Input) -> str | int:
        return self.part_one(input)

    def part_two_alt(self, input: Input) -> str | int:
        return self.part_two(input)

    def get_input(self, year: int, day: int) -> Input:
        return Input(data=aocd.get_data(day=day, year=year))

    def cli(self: Self) -> Callable[[], None]:
        puzzle_runner = self

        @click.command()
        @click.option("--p1", "-1", is_flag=True, help="Run part one")
        @click.option("--p2", "-2", is_flag=True, help="Run part two")
        @click.option("--test", "-t", is_flag=True, help="Run tests")
        @click.option("--alt", "-a", is_flag=True, help="Run alternative")
        @click.option(
            "--fail-fast",
            "--ff",
            "-f",
            is_flag=True,
            help="Stop on first test failure (implies --test)",
        )
        def entrypoint(p1: bool, p2: bool, test: bool, fail_fast: bool, alt: bool) -> None:
            if not (p1 or p2 or test):
                # default, run it all
                p1 = p2 = test = True

            part_1 = puzzle_runner.part_one_alt if alt else puzzle_runner.part_one
            part_2 = puzzle_runner.part_two_alt if alt else puzzle_runner.part_two

            if test or fail_fast:
                click.secho("Running tests...", fg="blue")

                def report(test_number: int, result: str, expected: str) -> bool:
                    if result != expected:
                        click.secho(
                            f"  {test_number}.  ❌ {result or '?'} != {expected}", fg="red"
                        )
                        return False
                    click.secho(f"  {test_number}.  ✅ {result} == {expected}", fg="green")
                    return True

                test_puzzle = Input(data=puzzle_runner.test_input)
                t1 = str(part_1(test_puzzle))
                if not report(1, t1, puzzle_runner.test_answers[0]) and fail_fast:
                    return

                test_puzzle = Input(data=puzzle_runner.test_input_2 or puzzle_runner.test_input)
                t2 = str(part_2(test_puzzle))
                if not report(2, t2, puzzle_runner.test_answers[1]) and fail_fast:
                    return

            if not (p1 or p2):
                return

            input_data = puzzle_runner.get_input(puzzle_runner.year, puzzle_runner.day)
            click.echo()
            if p1:
                click.secho("Part 1: ", fg="blue", nl=False)
                click.echo(part_1(input_data))
            if p2:
                click.secho("Part 2: ", fg="blue", nl=False)
                click.echo(part_2(input_data))

        return entrypoint()  # type: ignore [no-any-return]
