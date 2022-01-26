from __future__ import annotations

import dataclasses
import typing as t
from collections import deque
from copy import deepcopy

import networkx as nx

G = t.TypeVar("G")
Point = tuple[float, float]
Point3d = tuple[float, float, float]
SENTINEL = object()


def int_numbers(input_data: str, sep=None) -> t.List[int]:
    if sep is None:
        return [int(num) for num in input_data.splitlines() if num.strip()]
    return [int(num) for num in input_data.split(sep) if num.strip()]


def first(i: t.Iterable[G]) -> G:
    """Goes boom if empty"""
    return next(iter(i))


def only(i: t.Iterable[G]) -> G:
    """Goes boom if len != 1"""
    consumed = list(i)
    if len(consumed) != 1:
        raise ValueError(f"i had {len(consumed)} values")
    return consumed[0]


def sort_by_length(iterables: t.Iterable[t.Sequence[G]]) -> t.Iterable[t.Sequence[G]]:
    return sorted(iterables, key=len)


def line_algorithm(start: Point, end: Point) -> t.Iterable[Point]:
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


def sum_points(*points: Point) -> Point:
    return sum(p[0] for p in points), sum(p[1] for p in points)


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
UPLEFT = sum_points(UP, LEFT)
UPRIGHT = sum_points(UP, RIGHT)
DOWNLEFT = sum_points(DOWN, LEFT)
DOWNRIGHT = sum_points(DOWN, RIGHT)
DIRECTIONS_4: list[Point] = [UP, RIGHT, DOWN, LEFT]
DIRECTIONS_8: list[Point] = [UPLEFT, UP, UPRIGHT, RIGHT, DOWNRIGHT, DOWN, DOWNLEFT, LEFT]


@dataclasses.dataclass
class Grid(t.Generic[G]):
    points: dict[Point, G]

    def __init__(self, rows: t.Iterable[t.Iterable[G]], pad_with: t.Optional[G] = None):
        self.points = {}
        self.pad_with = pad_with
        for y, row in enumerate(rows):
            for x, item in enumerate(row):
                self.points[(x, y)] = item

    @classmethod
    def from_number_string(cls, data: str, separator=None, pad_with: t.Optional[G] = None):
        if separator:
            return Grid(
                rows=((int(n) for n in row.split(separator)) for row in data.splitlines()),
                pad_with=pad_with,
            )
        return Grid(rows=((int(n) for n in row) for row in data.splitlines()), pad_with=pad_with)

    def __len__(self) -> int:
        return self.points.__len__()

    def __iter__(self):
        return self.points.__iter__()

    def __next__(self):
        return self.points.__next__()

    def __getitem__(self, index: Point) -> G:
        return self.points[index]

    def __setitem__(self, index: Point, value: G):
        self.points[index] = value

    @property
    def _directions(self) -> list[Point]:
        return DIRECTIONS_4

    @property
    def _directions_diag(self) -> list[Point]:
        return DIRECTIONS_8

    def get_neighbours(self, point: Point, diag: bool = False) -> t.Iterable[Point]:
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
        comparison_func: t.Callable[[tuple[Point, G], list[tuple[Point, G]]], bool],
        diagonal: bool = False,
    ) -> t.Iterable[tuple[Point, G]]:
        for point in self.points.keys():
            neighbours = [(n, self.points[n]) for n in self.get_neighbours(point, diag=diagonal)]
            if comparison_func((point, self.points[point]), neighbours):
                yield point, self.points[point]

    def collect_recursive(
        self,
        points: t.Iterable[Point],
        comparison_func: t.Callable[[tuple[Point, G], list[tuple[Point, G]]], bool],
        diagonal: bool = False,
    ) -> t.Iterable[tuple[Point, G]]:
        queue = deque(list(points))
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

    def to_graph(self, diagonal=False, weighted=True, directed=True) -> nx.Graph:
        graph = nx.DiGraph() if directed else nx.Graph()
        for point in self:
            neighbours = self.get_neighbours(point, diag=diagonal)
            for nb in neighbours:
                if weighted:
                    graph.add_edge(point, nb, weight=self[nb])
                else:
                    graph.add_edge(point, nb)
        return graph

    def replicate(self, right: int, down: int) -> Grid:
        grid: Grid = Grid([])
        size = max(self)
        length_x = size[0] + 1
        length_y = size[1] + 1
        grid = deepcopy(self)
        for y in range(length_y):
            for x in range(length_x):
                for d in range(0, down):
                    for r in range(0, right):
                        grid[length_x * r + x, length_y * d + y] = self[x, y]
        return grid

    def add_padding(self, value: G):
        low = min(self)
        high = max(self)
        new_top = low[1] - 1
        new_bottom = high[1] + 1
        new_left = low[0] - 1
        new_right = high[0] + 1
        for y in range(new_top, new_bottom + 1):
            if y in (new_top, new_bottom):
                for x in range(new_left, new_right + 1):
                    self[x, y] = value
            else:
                self[new_left, y] = value
                self[new_right, y] = value

    def print(self):
        gmin = min(self)
        gmax = max(self)
        for y in range(gmin[1], gmax[1] + 1):
            line = [str(self[x, y]) for x in range(gmin[0], gmax[0] + 1)]
            print("".join(line))
        print()

    def print_line(self, y: int):
        gmin = min(self)
        gmax = max(self)
        print("".join([str(self[x, y]) for x in range(gmin[0], gmax[0] + 1)]))


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
