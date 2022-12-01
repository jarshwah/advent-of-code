import aocd
import utils


def part_one(data: str) -> int:
    """
    Find the sum of calories of the elf holding the most calories.
    """
    return max(sum(group) for group in utils.Input(data).group().integers)


def part_two(data: str) -> int:
    """
    Find the sum of the caolories of the top 3 elves holding the most calories.
    """
    return sum(sorted((sum(group) for group in utils.Input(data).group().integers))[-3:])


def test():
    test_input = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 24000, answer_1
    assert answer_2 == 45000, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=1, year=2022)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
