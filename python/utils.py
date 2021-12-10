import dataclasses
import typing as t
from collections import deque

G = t.TypeVar("G")
Point = tuple[float, float]


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


@dataclasses.dataclass
class Grid(t.Generic[G]):
    points: dict[Point, G]

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UPLEFT = sum_points(UP, LEFT)
    UPRIGHT = sum_points(UP, RIGHT)
    DOWNLEFT = sum_points(DOWN, LEFT)
    DOWNRIGHT = sum_points(DOWN, RIGHT)

    def __init__(self, rows: t.Iterable[t.Iterable[G]]):
        self.points = {}
        for y, row in enumerate(rows):
            for x, item in enumerate(row):
                self.points[(x, y)] = item

    @property
    def _directions(self) -> list[Point]:
        return [self.UP, self.DOWN, self.LEFT, self.RIGHT]

    @property
    def _directions_diag(self) -> list[Point]:
        return self._directions + [self.UPLEFT, self.DOWNLEFT, self.UPRIGHT, self.DOWNRIGHT]

    def get_neighbours(self, point: Point, diag: bool = False) -> t.Iterable[Point]:
        directions = self._directions_diag if diag else self._directions
        for d in directions:
            p = sum_points(point, d)
            if p in self.points:
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
        point: Point,
        comparison_func: t.Callable[[tuple[Point, G], list[tuple[Point, G]]], bool],
        diagonal: bool = False,
    ) -> t.Iterable[tuple[Point, G]]:
        queue = deque([point])
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
