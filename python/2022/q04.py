import aocd
import utils


def part_one(raw: str) -> int:
    """Find pairs that fully overlap"""
    pairs = utils.Input(raw).split().parse("{:d}-{:d},{:d}-{:d}")
    return sum(
        lmin <= rmin <= rmax <= lmax or rmin <= lmin <= lmax <= rmax
        for lmin, lmax, rmin, rmax in pairs
    )


def part_two(raw: str) -> int:
    """Find pairs that partially overlap"""
    pairs = utils.Input(raw).split().parse("{:d}-{:d},{:d}-{:d}")
    return sum(
        bool(set(range(lmin, lmax + 1)).intersection(set(range(rmin, rmax + 1))))
        for lmin, lmax, rmin, rmax in pairs
    )


def test():
    test_input = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 2, answer_1
    assert answer_2 == 4, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=4, year=2022)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
