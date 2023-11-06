import typing as t
from collections import defaultdict, deque

import aocd


def solve(data: str, allow_twice: bool) -> int:
    nodes: dict[str, list[str]] = defaultdict(list)
    for line in data.splitlines():
        L, R = line.split("-")
        nodes[L].append(R)
        nodes[R].append(L)
    num = 0
    node: str = "start"
    queue: t.Deque[tuple[str, set[str], bool]] = deque([(node, set(), False)])
    while queue:
        curr, visited, twice = queue.popleft()
        visited = set(visited)
        if curr == "end":
            num += 1
            continue
        for n in nodes[curr]:
            if n.islower() and n in visited:
                if allow_twice:
                    if not twice and n not in ["start", "end"]:
                        queue.append((n, visited, True))
                continue
            visited.add(curr)
            queue.append((n, visited, twice))
    return num


def part_one(data: str) -> int:
    return solve(data, allow_twice=False)


def part_two(data: str) -> int:
    return solve(data, allow_twice=True)


def test():
    test_input = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 19, answer_1
    assert answer_2 == 103, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=12, year=2021)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
