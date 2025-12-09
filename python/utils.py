from __future__ import annotations

import contextlib
import dataclasses
import itertools
import math
import multiprocessing
import pathlib
import re
from collections import deque
from collections.abc import Callable, Collection, Hashable, Iterable, Iterator, Sequence
from contextlib import contextmanager
from copy import deepcopy
from enum import Enum, StrEnum
from functools import cached_property
from typing import Any, Generator, Self, TypedDict, TypeVar

import aocd
import networkx as nx
import parse
import rich_click as click
from rich import live, panel

type Point = tuple[int, int]
type Point3d = tuple[int, int, int]
type Point4d = tuple[int, int, int, int]
type PointNd = tuple[int, ...]
SENTINEL = object()


A = TypeVar("A")


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

    def scan_ints(self) -> Sequence[int]:
        return scan_ints(self.data)

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

    def replace(self, old: str, new: str) -> Self:
        self.data = self.data.replace(old, new)
        return self


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

    def scan_ints(self) -> Sequence[Sequence[int]]:
        return [inp.scan_ints() for inp in self.data]

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

    def scan_ints(self) -> Sequence[Sequence[Sequence[int]]]:
        return [inp.scan_ints() for inp in self.data]

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


SCANNER = re.compile(r"-?[0-9]+")


def scan_ints(data: str) -> Sequence[int]:
    return list(map(int, SCANNER.findall(data)))


def int_numbers(input_data: str, sep: str | None = None) -> Sequence[int]:
    """Transform a line of numbers into a list of integers"""
    if sep is None:
        return [int(num) for num in input_data.splitlines() if num.strip()]
    return [int(num) for num in input_data.split(sep) if num.strip()]


def flatten[T](iterable: Iterable[Iterable[T]]) -> Sequence[T]:
    """Flatten an iterable of iterables into a single list"""
    return [item for sublist in iterable for item in sublist]


def first[T](i: Iterable[T]) -> T:
    """Return the first item of the iterator or exception if empty"""
    return next(iter(i))


def only[T](i: Iterable[T]) -> T:
    """Return the only item of the iterator or exception if not exactly one item"""
    consumed = list(i)
    if len(consumed) != 1:
        raise ValueError(f"i had {len(consumed)} values")
    return consumed[0]


def binary_search(low: int, high: int, condition: Callable[[int], bool]) -> int:
    """
    Use binary search to find the target matching the condition.
    """

    found = low - 1
    while True:
        if low == high:
            break
        search = (low + high) // 2
        ok = condition(search)
        if ok:
            low = search + 1
            found = search
        else:
            high = search
    return found


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


def manhattan_2d(p1: Point, p2: Point) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


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


def move(position: Point, direction: Point) -> Point:
    """
    Move a point in a direction.

    >>> move((10, 10), RIGHT)
    (10, 11)
    """
    return point_add(position, direction)


def moves(position: Point, direction: str) -> Point:
    """
    Move a point in a direction.

    >>> moves((10, 10), ">")
    (10, 11)
    """
    return move(position, DIRECTIONS_ASCII[direction])


def moved(from_position: Point, to_position: Point) -> str:
    return DIRECTIONS_ASCII_REVERSE[point_subtract(to_position, from_position)]


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
DIRECTIONS_ASCII: dict[str, Point] = {
    "^": UP,
    "v": DOWN,
    "<": LEFT,
    ">": RIGHT,
}
DIRECTIONS_ASCII_REVERSE = {v: k for k, v in DIRECTIONS_ASCII.items()}
DIRECTIONS_LETTERS: dict[str, Point] = {
    "L": LEFT,
    "R": RIGHT,
    "D": DOWN,
    "U": UP,
}


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


def internal_corners(group: set[Point]) -> Collection[Point]:
    """
    Given a group of points, find the internal corners.

    An internal corner is a missing diagonal surrounded by 3 points.

                X .
                . .
    """
    UL, UP, UR, R, DR, D, DL, L = DIRECTIONS_8
    corners = []
    add = point_add
    for p in group:
        if add(p, L) in group and add(p, UP) in group and (C := add(p, UL)) not in group:
            # X .
            # . .
            corners.append(C)
        if add(p, UP) in group and add(p, R) in group and (C := add(p, UR)) not in group:
            # . X
            # . .
            corners.append(C)
        if add(p, R) in group and add(p, D) in group and (C := add(p, DR)) not in group:
            # . .
            # . X
            corners.append(C)
        if add(p, D) in group and add(p, L) in group and (C := add(p, DL)) not in group:
            # . .
            # X .
            corners.append(C)
    return corners


def external_corners(group: set[Point]) -> Sequence[Point]:
    """
    Given a group of points, find the external corners.

    A point in an external corner will be in the return value N times if it represents N corners.

    An external corner is a point missing neighbours in two successive directions.

          ? 1     . is the point being checked (and returned as a corner)
        - . ?     ? are the sides being checked
          |       1 is the corner being checked
    """
    U, R, D, L = DIRECTIONS_4
    corners = []
    add = point_add
    for p in group:
        if add(p, U) not in group and add(p, R) not in group:
            #   ? X
            # - . ?
            #   |
            corners.append(p)
        if add(p, R) not in group and add(p, D) not in group:
            # X .
            corners.append(p)
        if add(p, D) not in group and add(p, L) not in group:
            # .
            # X
            corners.append(p)
        if add(p, L) not in group and add(p, U) not in group:
            # .
            # X
            corners.append(p)
    return corners


def all_corners(group: set[Point]) -> Collection[Point]:
    """
    Get all corners of a group of points.
    Assumes the group is a connected set.

    eg: 6 corners:

        11..
        .11.
        .1.

    """
    return list(external_corners(group)) + list(internal_corners(group))


def num_sides_of_group(group: set[Point]) -> int:
    """
    Get the number of sides of a group of points.

    The number of sides is equal to the number of external corners.

    Assumes the group is a connected set.
    """
    return len(all_corners(group))


def dijkstra_best_score[T](
    grid: Grid[T],
    start: Point,
    target: Point,
    direction: Point = UP,
    unmovable: T | None = None,
) -> dict[Point, int]:
    """
    Find the best score to reach the target from the start.

    Returns a dictionary of the best score to reach each point from the start.
    """
    import heapq

    type Steps = int
    type Current = Point

    heap: list[tuple[Steps, Current]] = []
    # add whatever other vars I might need to track like the Path
    heapq.heappush(heap, (0, start))
    seen: dict[Point, Steps] = {}
    while heap:
        num_steps, position = heapq.heappop(heap)
        if position == target:
            seen[position] = min(seen.get(position, int(1e9)), num_steps)
            continue
        if grid[position] == unmovable:
            continue
        if position in seen and seen[position] <= num_steps:
            continue
        seen[position] = num_steps
        for new_position in grid.get_neighbours(position):
            heapq.heappush(heap, (num_steps + 1, new_position))
    return seen


def dijkstra_shortest_path[T](
    grid: Grid[T],
    start: Point,
    target: Point,
    direction: Point = UP,
    unmovable: T | None = None,
) -> list[Point]:
    """
    Find the shortest path between START and TARGET.
    """
    import heapq

    type Steps = int
    type Current = Point
    type Path = list[Point]

    heap: list[tuple[Steps, Current, Path]] = []
    # add whatever other vars I might need to track like the Path
    heapq.heappush(heap, (0, start, []))
    seen: dict[Point, tuple[Steps, Path]] = {}
    while heap:
        num_steps, position, path = heapq.heappop(heap)
        path.append(position)
        if position == target:
            s_steps, _ = seen.get(position, (int(1e9), []))
            if num_steps <= s_steps:
                seen[position] = (num_steps, path)
            continue
        if grid[position] == unmovable:
            continue
        if position in seen and seen[position][0] <= num_steps:
            continue
        seen[position] = num_steps, path
        for new_position in grid.get_neighbours(position):
            heapq.heappush(heap, (num_steps + 1, new_position, path[:]))
    return seen[target][1]


def line_overlaps(l1: Point, l2: Point) -> bool:
    # We allow the line to *touch* > but not *cross* >=
    return max(l1) > min(l2) and max(l2) > min(l1)


@dataclasses.dataclass(frozen=True, slots=True)
class Rect:
    x1: int
    x2: int
    y1: int
    y2: int

    @classmethod
    def from_corners(cls, p1: Point, p2: Point) -> Rect:
        return Rect(min(p1[0], p2[0]), max(p1[0], p2[0]), min(p1[1], p2[1]), max(p1[1], p2[1]))

    @property
    def area(self) -> int:
        return (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1)

    def overlaps(self, other: Rect) -> bool:
        # fmt: off
        return (
            line_overlaps((self.x1, self.x2), (other.x1, other.x2)) and
            line_overlaps((self.y1, self.y2), (other.y1, other.y2)
            )
        )
        # fmt: on


H = TypeVar("H", bound=Hashable)
type Tree[H] = set[H]
type Forest[H] = dict[H, Tree[H]]


@dataclasses.dataclass()
class DisjointSet[H]:
    """
    DisjointSet allows for Union-Find to connect sets together.
    """

    forest: dict[H, set[H]]

    def __init__(self, forest: Forest[H]) -> None:
        self.forest = forest

    @classmethod
    def from_iterable(cls, nodes: Sequence[H]) -> DisjointSet[H]:
        return DisjointSet({n: {n} for n in nodes})

    def find(self, node: H) -> H:
        for parent in self.forest:
            if node in self.forest[parent]:
                return parent
        raise ValueError("Not in forest")

    def union(self, from_node: H, to_node: H) -> H:
        from_parent = self.find(from_node)
        to_parent = self.find(to_node)
        if from_parent != to_parent:
            self.forest[to_parent] |= self.forest[from_parent]
            del self.forest[from_parent]
        return to_parent

    def size(self) -> int:
        return len(self.forest)

    def trees(self) -> Sequence[set[H]]:
        return list(self.forest.values())

    def connected(self, from_node: H, to_node: H) -> bool:
        return self.find(from_node) == self.find(to_node)


@dataclasses.dataclass
class Grid[T]:
    """
    Models a grid of (row, column) points with a value at each point.
    """

    points: dict[Point, T]
    _drawer: GridDrawer
    _animating: bool = False

    def __init__(self, rows: Iterable[Iterable[T]], pad_with: T | None = None):
        self.points = {}
        self.pad_with = pad_with
        for r, row in enumerate(rows):
            for c, item in enumerate(row):
                self.points[(r, c)] = item
        self._animating = False
        self._drawer = GridDrawer(frames=[])

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
        if index not in self.points:
            with contextlib.suppress(AttributeError):
                del self.width
            with contextlib.suppress(AttributeError):
                del self.height
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
        """
        return max(p[1] for p in self.points) + 1

    @cached_property
    def height(self) -> int:
        """
        How tall the grid is.
        """
        return max(p[0] for p in self.points) + 1

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

    def find_all(self, value: T) -> Iterable[Point]:
        """
        Find the first point with the given value.
        """
        []
        for point, v in self.points.items():
            if v == value:
                yield point

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

    def collect_while(
        self,
        start: Point,
        compare: Callable[[Grid[T], Point, Point], bool],
        diagonal: bool = False,
    ) -> Iterable[Point]:
        """
        Collect all unique points that meet the comparison function from a starting point.

        This is equivalent to a flood fill.
        """
        queue = deque([start])
        seen = set()
        found = {start}
        while queue:
            p = queue.popleft()
            if p in seen:
                continue
            seen.add(p)
            for nb in self.get_neighbours(p, diag=diagonal):
                if compare(self, p, nb):
                    found.add(nb)
                    queue.append(nb)
        return found

    flood_fill = collect_while

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
        assert right > 1 or down > 1, "Replication must be greater than 1 in at least one direction"
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

    def save_frame(self, header: str = "") -> None:
        self._drawer.frames.append(Frame(content=list(self.strings()), header=header))

    def draw_frames(self, color_map: ColorMap) -> None:
        self._drawer.draw(color_map)

    def render_video(self, name: str, framerate: int = 10) -> None:
        self._drawer.create_mp4(name, framerate)

    @contextmanager
    def animate(self, on: bool = True) -> Iterator[GridAnimator]:
        animator = GridAnimator(on)
        with animator.animate(self):
            yield animator

    def hash_key(self) -> str:
        """
        Make a hash key out of the content of the grid, so that it's hashable.
        """
        return "".join(self.strings())


class NotAnimating(Exception):
    pass


class GridAnimator:
    def __init__(self, on: bool = True) -> None:
        self.animating = on
        self.renderer: live.Live | None = None
        self.header: str | None = None

    def set_header(self, header: str) -> None:
        self.header = header

    @contextmanager
    def animate(self, grid: Grid[A]) -> Iterator[Self]:
        if self.animating:
            with live.Live(self._get_content(grid), auto_refresh=False) as renderer:
                self.renderer = renderer
                yield self
            self.renderer = None
        else:
            yield self

    def update(self, grid: Grid[A], header: str | None = None) -> None:
        if not self.renderer:
            return
        self.header = header
        self.renderer.update(self._get_content(grid), refresh=True)

    def _get_content(self, grid: Grid[A]) -> panel.Panel:
        s = ""
        for row in grid.strings():
            s += row
            s += "\n"
        return panel.Panel.fit(s, title=self.header)


BLOCK = "#"
SPACE = " "
LINE_COLOR = (50, 50, 50)
BACKGROUND_COLOR = (0, 0, 0)


class ColorRGB(Enum):
    Black = (0, 0, 0)
    White = (255, 255, 255)
    Yellow = (255, 255, 0)
    Grey = (192, 192, 192)
    GreyDark = (96, 96, 96)
    PurpleLight = (192, 192, 255)


DefaultColor = ColorRGB.GreyDark
BackgroundColor = ColorRGB.Black

type RGB = tuple[int, int, int]
type ColorMap = dict[str | int, RGB]

DEFAULT_COLOR_MAP: ColorMap = {
    0: ColorRGB.Black.value,
    " ": ColorRGB.Black.value,
    ".": ColorRGB.Black.value,
    1: ColorRGB.White.value,
    "#": ColorRGB.White.value,
    "Star": ColorRGB.Yellow.value,
    "star": ColorRGB.Yellow.value,
    "Target": ColorRGB.PurpleLight.value,
    "target": ColorRGB.PurpleLight.value,
    "Gray": ColorRGB.Grey.value,
    "DarkGray": ColorRGB.GreyDark.value,
}

DEFAULT_DISP_MAP: dict[str | int, str] = {
    " ": SPACE,
    0: SPACE,
    ".": SPACE,
    "#": BLOCK,
    1: BLOCK,
}


@dataclasses.dataclass
class Frame:
    content: list[str]
    header: str


class RenderFrameData(TypedDict, total=True):
    frame: Frame
    frame_num: int
    color_map: ColorMap
    target_dir: str


@dataclasses.dataclass
class GridDrawer:
    frames: list[Frame] = dataclasses.field(default_factory=list)

    def delete_rendered_frames(self) -> None:
        target_dir = pathlib.Path("./animations/")
        if not target_dir.exists():
            return
        for existing in target_dir.glob("*.png"):
            if existing.is_file():
                existing.unlink()

    def draw(self, color_map: ColorMap = DEFAULT_COLOR_MAP) -> None:
        target_dir = pathlib.Path("./animations/")
        if not target_dir.exists():
            target_dir.mkdir(parents=True, exist_ok=True)
        self.delete_rendered_frames()

        todo: list[RenderFrameData] = [
            {
                "color_map": color_map,
                "frame": frame,
                "frame_num": idx,
                "target_dir": str(target_dir.absolute()),
            }
            for idx, frame in enumerate(self.frames, 1)
        ]
        total = len(todo)
        percent_done = 0
        with multiprocessing.Pool() as pool:
            for result in pool.imap_unordered(render_frame, todo):
                done = total - len(todo)
                perc = math.floor((done / total) * 100)
                if perc > percent_done and perc % 5 == 0:
                    percent_done = perc
                    print(f"{done}/{total} ({percent_done}%): {result}")

    def create_mp4(self, name: str, rate: int = 10) -> None:
        import subprocess

        target_dir = pathlib.Path("./animations").resolve().absolute()
        if not target_dir.exists():
            raise ValueError("Path does not exist for rendering the movie")

        cmd = [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-f",
            "image2",
            "-framerate",
            str(rate),
            "-i",
            "./animations/frame_%05d.png",
            "-c:v",
            "libx264",
            "-profile:v",
            "main",
            "-pix_fmt",
            "yuv420p",
            "-vf",
            "pad=ceil(iw/2)*2:ceil(ih/2)*2",
            "-an",
            "-movflags",
            "+faststart",
            str(target_dir / f"animation_{name}.mp4"),
        ]
        print("$ " + " ".join(cmd))
        subprocess.check_call(cmd)
        self.delete_rendered_frames()

    def __deepcopy__(self, memo: Any) -> Self:
        # Do not copy all of the frames.
        return self


def render_frame(render_frame: RenderFrameData) -> None:
    from PIL import Image, ImageDraw

    frame = render_frame["frame"]
    frame_num = render_frame["frame_num"]
    colors = render_frame["color_map"]
    target_dir = render_frame["target_dir"]

    height = len(frame.content)
    width = len(frame.content[0])

    border_size = 5
    im = Image.new(
        "RGB",
        (
            width + (border_size * 2) + 1,
            height + (border_size * 2) + 1,
        ),
        color=BACKGROUND_COLOR,
    )
    draw = ImageDraw.Draw(im, "RGBA")

    # Draw the border
    draw.rectangle(
        ((border_size, border_size), (border_size + width, border_size + height)),
        ColorRGB.GreyDark.value,
        ColorRGB.GreyDark.value,
    )
    for y, row in enumerate(frame.content):
        for x, ch in enumerate(row):
            color = colors.get(ch, DefaultColor.value)
            draw.rectangle(
                (
                    (border_size + x + 1, border_size + y + 1),
                    (border_size + x + 1, border_size + y + 1),
                ),
                color,
                color,
            )

    # Do scaling later.
    scale = 10
    im = im.resize(
        (int(im.width * scale), int(im.height * scale)), resample=Image.Resampling.LANCZOS
    )

    im.save(pathlib.Path(target_dir) / f"frame_{frame_num:05d}.png")


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


class Color(StrEnum):
    BLACK = "black"
    WHITE = "white"
    RED = "red"
    RED_BRIGHT = "bright_red"
    GREEN = "green"
    GREEN_BRIGHT = "bright_green"
    YELLOW = "yellow"
    YELLOW_BRIGHT = "bright_yellow"
    BLUE = "blue"
    BLUE_BRIGHT = "blue1"  # #0000ff
    BLUE_VIOLET = "blue_violet"  # #5f00ff
    PURPLE_4 = "purple_4"  # #5f00af

    def colorize(self, text: str) -> str:
        return f"[bold {self.value}]{text}[/bold {self.value}]"


@dataclasses.dataclass
class Puzzle:
    year: int
    day: int
    test_input: str = ""
    test_input_2: str = ""
    test_answers: tuple[str, str] = ("", "")
    both: bool = False
    testing: bool = False
    no_tests: bool = False
    animate: bool = False

    def part_one(self, input: Input) -> str | int:
        return ""

    def part_two(self, input: Input) -> str | int:
        return ""

    def part_one_alt(self, input: Input) -> str | int:
        return self.part_one(input)

    def part_two_alt(self, input: Input) -> str | int:
        return self.part_two(input)

    def both_parts(self, input: Input) -> tuple[str | int, str | int]:
        return "", ""

    def get_input(self, year: int, day: int) -> Input:
        return Input(data=aocd.get_data(day=day, year=year))

    def cli(self: Self) -> Callable[[], None]:
        puzzle_runner = self

        @click.command()
        @click.option("--p1", "-1", is_flag=True, help="Run part one")
        @click.option("--p2", "-2", is_flag=True, help="Run part two")
        @click.option("--animate", is_flag=True, help="Run the animation if one exists")
        @click.option("--test", "-t", is_flag=True, help="Run tests")
        @click.option("--alt", "-a", is_flag=True, help="Run alternative")
        @click.option(
            "--fail-fast",
            "--ff",
            "-f",
            is_flag=True,
            help="Stop on first test failure (implies --test)",
        )
        def entrypoint(
            p1: bool, p2: bool, animate: bool, test: bool, fail_fast: bool, alt: bool
        ) -> None:
            if not (p1 or p2 or test):
                # default, run it all
                p1 = p2 = test = True

            puzzle_runner.animate = animate

            part_1 = puzzle_runner.part_one_alt if alt else puzzle_runner.part_one
            part_2 = puzzle_runner.part_two_alt if alt else puzzle_runner.part_two

            if (test or fail_fast) and puzzle_runner.no_tests:
                click.secho("Skipping tests...", fg="blue")
            elif test or fail_fast:
                puzzle_runner.testing = True
                click.secho("Running tests...", fg="blue")

                def report(test_number: int, result: str, expected: str) -> bool:
                    label = f"  {test_number}{'a' if alt else ''}."
                    if expected == "no-answer":
                        click.secho(f"{label}  🦘 No Test Answer Available", fg="yellow")
                        return True
                    if result != expected:
                        click.secho(f"{label}  ❌ {result or '?'} != {expected}", fg="red")
                        return False
                    click.secho(f"{label}  ✅ {result} == {expected}", fg="green")
                    return True

                test_puzzle = Input(data=puzzle_runner.test_input)
                if puzzle_runner.both:
                    t1, t2 = puzzle_runner.both_parts(test_puzzle)
                    if (
                        not report(1, str(t1), puzzle_runner.test_answers[0])
                        or not report(2, str(t2), puzzle_runner.test_answers[1])
                        and fail_fast
                    ):
                        return
                else:
                    t1 = str(part_1(test_puzzle))
                    if not report(1, t1, puzzle_runner.test_answers[0]) and fail_fast:
                        return

                    test_puzzle = Input(data=puzzle_runner.test_input_2 or puzzle_runner.test_input)
                    t2 = str(part_2(test_puzzle))
                    if not report(2, t2, puzzle_runner.test_answers[1]) and fail_fast:
                        return

            # Undo the test flag.
            puzzle_runner.testing = False

            if not (p1 or p2 or puzzle_runner.both):
                return

            input_data = puzzle_runner.get_input(puzzle_runner.year, puzzle_runner.day)
            click.echo()
            a1: int | str = click.style("Skipped", fg="yellow")
            a2 = a1
            if puzzle_runner.both and (p1 or p2):
                a1, a2 = puzzle_runner.both_parts(input_data)
            else:
                if p1:
                    a1 = part_1(input_data)
                if p2:
                    a2 = part_2(input_data)
            alt_str = "a" if alt else ""
            click.secho(f"Part 1{alt_str}: ", fg="blue", nl=False)
            click.echo(a1)
            click.secho(f"Part 2{alt_str}: ", fg="blue", nl=False)
            click.echo(a2)

        return entrypoint()  # type: ignore [no-any-return]
