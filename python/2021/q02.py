import aocd


def part_one(data: list[str]) -> int:
    position = depth = 0
    for line in data:
        direction, units = line.split()
        units = int(units)
        match direction:
            case "forward":
                position += units
            case "down":
                depth += units
            case "up":
                depth -= units
    return position * depth


def part_two(data: list[str]) -> int:
    position = depth = aim = 0
    for line in data:
        direction, units = line.split()
        units = int(units)
        match direction:
            case "forward":
                position += units
                depth += units * aim
            case "down":
                aim += units
            case "up":
                aim -= units
    return position * depth


def test():
    test_input = """forward 5
down 5
forward 8
up 3
down 8
forward 2
"""
    answer_1 = part_one(test_input.splitlines())
    answer_2 = part_two(test_input.splitlines())
    assert answer_1 == 150, answer_1
    assert answer_2 == 900, answer_2


if __name__ == "__main__":
    test()

    data = aocd.get_data(day=2, year=2021).splitlines()
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
