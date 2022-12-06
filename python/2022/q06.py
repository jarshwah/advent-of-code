import aocd
from more_itertools import windowed


def part_one(raw: str) -> int:
    return find_marker(raw, 4)


def part_two(raw: str) -> int:
    return find_marker(raw, 14)


def find_marker(raw: str, marker: int) -> int:
    for idx, substr in enumerate(windowed(raw, marker)):
        if len(set(substr)) == marker:
            return idx + marker
    return 1


def test():
    answer_1 = part_one("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
    answer_2 = part_two("""nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg""")
    assert answer_1 == 11, answer_1
    assert answer_2 == 29, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=6, year=2022)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
