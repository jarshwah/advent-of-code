from __future__ import annotations

import dataclasses
import itertools
from collections import deque
from copy import deepcopy
from functools import cached_property
from typing import Callable, Generic, Iterable, Sequence, TypeVar

import networkx as nx
from parse import parse

G = TypeVar("G")
Point = tuple[float, float]
Point3d = tuple[float, float, float]
Point4d = tuple[float, float, float, float]
PointNd = TypeVar("PointNd", bound=tuple[float, ...])
SENTINEL = object()


@dataclasses.dataclass
class Input:
    data: str

    @property
    def string(self) -> str:
        return self.data

    @property
    def integer(self) -> int:
        return int(self.data)

    @property
    def number(self) -> int:
        return self.integer

    @property
    def float(self) -> float:
        return float(self.data)

    def parse(self, parser: str):
        return parse(parser, self.string)

    def lines(self) -> InputList:
        return self.split("\n")

    def split(self, sep: str | None = None) -> InputList:
        return InputList(data=[Input(data=token) for token in self.data.split(sep)])

    def group(self, group: str | None = "\n\n", sep: str | None = None) -> InputGroup:
        return self.split(group).split(sep)


@dataclasses.dataclass
class InputList:
    data: list[Input]

    @property
    def strings(self) -> list[str]:
        return [inp.string for inp in self.data]

    @property
    def integers(self) -> list[int]:
        return [inp.integer for inp in self.data]

    @property
    def numbers(self) -> list[int]:
        return self.integers

    @property
    def floats(self) -> list[float]:
        return [inp.float for inp in self.data]

    def parse(self, *parsers: str):
        results = []
        for s in self.strings:
            for p in parsers:
                if result := parse(p, s):
                    results.append(result)
                    break
            else:
                raise ValueError(f"{s} was not parsed")
        return results

    def split(self, sep: str | None = None) -> InputGroup:
        return InputGroup(data=[inp.split(sep) for inp in self.data])


@dataclasses.dataclass
class InputGroup:
    data: list[InputList]

    @property
    def strings(self) -> list[list[str]]:
        return [inp.strings for inp in self.data]

    @property
    def integers(self) -> list[list[int]]:
        return [inp.integers for inp in self.data]

    @property
    def numbers(self) -> list[list[int]]:
        return self.integers

    @property
    def floats(self) -> list[list[float]]:
        return [inp.floats for inp in self.data]

    @property
    def number_grid(self) -> Grid[int]:
        return Grid(rows=self.numbers)

    @property
    def string_grid(self) -> Grid[str]:
        return Grid(rows=self.strings)

    def parse(self, *parsers: str):
        return [inp.parse(*parsers) for inp in self.data]


def int_numbers(input_data: str, sep=None) -> list[int]:
    if sep is None:
        return [int(num) for num in input_data.splitlines() if num.strip()]
    return [int(num) for num in input_data.split(sep) if num.strip()]


def first(i: Iterable[G]) -> G:
    """Goes boom if empty"""
    return next(iter(i))


def only(i: Iterable[G]) -> G:
    """Goes boom if len != 1"""
    consumed = list(i)
    if len(consumed) != 1:
        raise ValueError(f"i had {len(consumed)} values")
    return consumed[0]


def sort_by_length(iterables: Iterable[Sequence[G]]) -> Iterable[Sequence[G]]:
    return sorted(iterables, key=len)


def line_algorithm(start: Point, end: Point) -> Iterable[Point]:
    """
    Finds all points between `start` and `end` points.
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


def split_list(items: list) -> tuple[list, list]:
    midpoint = len(items) // 2
    return items[:midpoint], items[midpoint:]


def partition(seq: Sequence[G], idx: int) -> tuple[Sequence[G], Sequence[G]]:
    return seq[:idx], seq[idx:]


def partition_middle(seq: Sequence[G]) -> tuple[Sequence[G], Sequence[G]]:
    midpoint = len(seq) // 2
    return seq[:midpoint], seq[midpoint:]


def chunked(
    it: Iterable[G], n: int, fillvalue: G | None = None
) -> Iterable[Iterable[G]]:
    return itertools.zip_longest(*[iter(it)] * n, fillvalue=fillvalue)


def stepped_sum(start: int, end: int) -> int:
    """
    Compute the sum difference of integers between two numbers

    ie: 2 -> 7
        1 + 2 + 3 + 4 + 5 == 15
    """
    return triangle_number(abs(start - end))


def triangle_number(n: int) -> int:
    """
    Compute the triange number

    The triangular number of 7 is 28

    1 + 2 + 3 + 4 + 5 + 6 + 7
    """
    return n * (n + 1) // 2


def triange_number_2(n: int) -> int:
    """
    Compute the 2-triangle number

    The triangular number of 7 is 49

    1 + 3 + 5 + 7 + 9 + 11 + 13
    """
    return n**2


def manhattan(p1: PointNd, p2: PointNd) -> int:
    return sum(abs(a - b) for a, b in zip(p1, p2, strict=True))  # type: ignore


def point_subtract(p1: PointNd, p2: PointNd) -> PointNd:
    return tuple(a - b for a, b in zip(p1, p2, strict=True))  # type: ignore


def point_add(p1: PointNd, p2: PointNd) -> PointNd:
    return tuple(a + b for a, b in zip(p1, p2, strict=True))  # type: ignore


def sum_points(*points: Point) -> Point:
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
DIRECTIONS_4: list[Point] = [UP, RIGHT, DOWN, LEFT]
DIRECTIONS_8: list[Point] = [
    UPLEFT,
    UP,
    UPRIGHT,
    RIGHT,
    DOWNRIGHT,
    DOWN,
    DOWNLEFT,
    LEFT,
]
DIRECTIONS_9: list[Point] = [
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


def neighbours(point: Point, directions: list[Point]) -> list[Point]:
    return [(point[0] + d[0], point[1] + d[1]) for d in directions]


@dataclasses.dataclass
class Grid(Generic[G]):
    points: dict[Point, G]

    def __init__(self, rows: Iterable[Iterable[G]], pad_with: G | None = None):
        self.points = {}
        self.pad_with = pad_with
        for r, row in enumerate(rows):
            for c, item in enumerate(row):
                self.points[(r, c)] = item

    @classmethod
    def from_number_string(cls, data: str, separator=None, pad_with: G | None = None):
        if separator:
            return Grid(
                rows=(
                    (int(n) for n in row.split(separator)) for row in data.splitlines()
                ),
                pad_with=pad_with,
            )
        return Grid(
            rows=((int(n) for n in row) for row in data.splitlines()), pad_with=pad_with
        )

    def get(self, key: G, default: G | None = None) -> G | None:
        return self.points.get(key, default)

    def __len__(self) -> int:
        return self.points.__len__()

    def __iter__(self):
        return self.points.__iter__()

    def __contains__(self, key: G) -> bool:
        return key in self.points

    def __getitem__(self, index: Point) -> G:
        return self.points[index]

    def __setitem__(self, index: Point, value: G):
        self.points[index] = value

    @cached_property
    def width(self) -> int:
        return max(self)[1] + 1

    @cached_property
    def height(self) -> int:
        return max(self)[0] + 1

    @property
    def _directions(self) -> list[Point]:
        return DIRECTIONS_4

    @property
    def _directions_diag(self) -> list[Point]:
        return DIRECTIONS_8

    def get_neighbours(self, point: Point, diag: bool = False) -> Iterable[Point]:
        directions = self._directions_diag if diag else self._directions
        for d in directions:
            p = sum_points(point, d)
            if p in self:
                yield p
            elif self.pad_with is not None:
                self[p] = self.pad_with
                yield p

    def search(
        self,
        comparison_func: Callable[[tuple[Point, G], list[tuple[Point, G]]], bool],
        diagonal: bool = False,
    ) -> Iterable[tuple[Point, G]]:
        for point in self.points.keys():
            neighbours = [
                (n, self.points[n]) for n in self.get_neighbours(point, diag=diagonal)
            ]
            if comparison_func((point, self.points[point]), neighbours):
                yield point, self.points[point]

    def collect_recursive(
        self,
        points: Iterable[Point],
        comparison_func: Callable[[tuple[Point, G], list[tuple[Point, G]]], bool],
        diagonal: bool = False,
    ) -> Iterable[tuple[Point, G]]:
        queue = deque(list(points))
        seen = set()
        found = set()
        while queue:
            p = queue.popleft()
            if p in seen:
                continue
            seen.add(p)
            neighbours = [
                (n, self.points[n]) for n in self.get_neighbours(p, diag=diagonal)
            ]
            if comparison_func((p, self.points[p]), neighbours):
                found.add(p)
                queue.extend([n[0] for n in neighbours])
        return [(f, self.points[f]) for f in found]

    def to_graph(
        self,
        diagonal=False,
        weighted=True,
        directed=True,
        is_connected_func: Callable[[G, G], bool] | None = None,
    ) -> nx.Graph:
        graph = nx.DiGraph() if directed else nx.Graph()
        for point in self:
            neighbours = self.get_neighbours(point, diag=diagonal)
            for nb in neighbours:
                if is_connected_func is None or is_connected_func(point, nb):
                    if weighted:
                        graph.add_edge(point, nb, weight=self[nb])
                    else:
                        graph.add_edge(point, nb)
        return graph

    def replicate(self, right: int, down: int) -> Grid:
        grid: Grid = Grid([])
        size = max(self)
        length_r = size[0] + 1
        length_c = size[1] + 1
        grid = deepcopy(self)
        for ri in range(length_r):
            for ci in range(length_c):
                for newri in range(down):
                    for newci in range(right):
                        grid[length_r * newri + ri, length_c * newci + ci] = self[
                            ri, ci
                        ]
        return grid

    def print(self, missing: G):
        rmin = min(self)[0]
        rmax = max(self)[0]
        cmin = min(node[1] for node in self)
        cmax = max(node[1] for node in self)

        for r in range(rmin, rmax + 1):
            line = [
                str(self.points.get((r, c), missing)) for c in range(cmin, cmax + 1)
            ]
            print("".join(line))
        print()


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
