import typing as t

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
