import typing as t

G = t.TypeVar("G")


def int_numbers(input_data: str) -> t.List[int]:
    return [int(num) for num in input_data.splitlines() if num.strip()]


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
