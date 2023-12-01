import aocd
import utils


def part_one(raw: str) -> int:
    data = utils.Input(raw)
    return 1


def part_two(raw: str) -> int:
    data = utils.Input(raw)
    return 1


def test():
    test_input = """"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 1, answer_1
    assert answer_2 == 1, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=1, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
